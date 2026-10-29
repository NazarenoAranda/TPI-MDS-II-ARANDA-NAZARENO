"""Pruebas unitarias del servicio y de las reglas, aisladas de la base de datos."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositorio_en_memoria import RepositorioEnMemoria
from solicitudes.errores import ErrorDeNegocio
from solicitudes.modelos import Estado, FiltroSolicitudes, NuevaSolicitud, Prioridad, TipoSolicitud
from solicitudes.reglas import ajustar_prioridad, validar_descripcion
from solicitudes.reporte import calcular_reporte
from solicitudes.repositorio_sqlite import RepositorioSqlite
from solicitudes.servicio import ServicioSolicitudes


def nueva(tipo="CERTIFICADO", prioridad="MEDIA", descripcion="Necesito algo", legajo="1001"):
    return NuevaSolicitud(legajo=legajo, tipo=tipo, prioridad=prioridad, descripcion=descripcion)


class PruebasDeReglas(unittest.TestCase):
    def test_reincorporacion_baja_sube_a_media_con_aviso(self):
        prioridad, aviso = ajustar_prioridad(TipoSolicitud.REINCORPORACION, Prioridad.BAJA)
        self.assertEqual(Prioridad.MEDIA, prioridad)
        self.assertIn("elevada", aviso)

    def test_consulta_alta_baja_a_media_con_aviso(self):
        prioridad, aviso = ajustar_prioridad(TipoSolicitud.CONSULTA, Prioridad.ALTA)
        self.assertEqual(Prioridad.MEDIA, prioridad)
        self.assertIn("reducida", aviso)

    def test_otras_combinaciones_no_se_modifican(self):
        self.assertEqual((Prioridad.ALTA, None), ajustar_prioridad(TipoSolicitud.EQUIVALENCIA, Prioridad.ALTA))

    def test_descripcion_limite_200_es_valida_y_201_no(self):
        self.assertEqual(200, len(validar_descripcion("a" * 200)))
        with self.assertRaises(ErrorDeNegocio):
            validar_descripcion("a" * 201)

    def test_descripcion_vacia_o_con_espacios_es_invalida(self):
        with self.assertRaises(ErrorDeNegocio):
            validar_descripcion("   ")

    def test_parseo_ignora_mayusculas_y_espacios(self):
        self.assertEqual(Estado.EN_PROCESO, Estado.desde_texto("  en_proceso "))

    def test_parseo_invalido_lista_valores_validos(self):
        with self.assertRaises(ErrorDeNegocio) as ctx:
            TipoSolicitud.desde_texto("foo")
        self.assertIn("CERTIFICADO, EQUIVALENCIA, REINCORPORACION, CONSULTA", str(ctx.exception))


class PruebasDelServicio(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioEnMemoria()
        self.servicio = ServicioSolicitudes(self.repo, reloj=lambda: "2026-01-01 00:00:00")

    def test_registrar_crea_solicitud_nueva_sin_responsable(self):
        resultado = self.servicio.registrar(nueva())
        solicitud = self.repo.obtener_solicitud(resultado.id)
        self.assertEqual(Estado.NUEVA, solicitud.estado)
        self.assertIsNone(solicitud.responsable_id)

    def test_registrar_estudiante_inexistente_falla(self):
        with self.assertRaises(ErrorDeNegocio):
            self.servicio.registrar(nueva(legajo="9999"))

    def test_registrar_aplica_ajuste_de_prioridad(self):
        resultado = self.servicio.registrar(nueva(tipo="reincorporacion", prioridad="baja"))
        self.assertEqual(Prioridad.MEDIA, resultado.prioridad)
        self.assertIsNotNone(resultado.aviso)

    def test_no_se_puede_pasar_a_en_proceso_sin_responsable(self):
        id_ = self.servicio.registrar(nueva()).id
        with self.assertRaises(ErrorDeNegocio):
            self.servicio.cambiar_estado(id_, "EN_PROCESO")

    def test_asignar_responsable_pasa_nueva_a_en_proceso(self):
        id_ = self.servicio.registrar(nueva()).id
        resultado = self.servicio.asignar_responsable(id_, 1)
        self.assertTrue(resultado.paso_a_en_proceso)
        self.assertEqual(Estado.EN_PROCESO, self.repo.obtener_solicitud(id_).estado)

    def test_reasignar_no_cambia_estado_ya_avanzado(self):
        id_ = self.servicio.registrar(nueva()).id
        self.servicio.asignar_responsable(id_, 1)
        self.servicio.cambiar_estado(id_, "RESUELTA")
        resultado = self.servicio.asignar_responsable(id_, 2)
        self.assertFalse(resultado.paso_a_en_proceso)
        self.assertEqual(Estado.RESUELTA, self.repo.obtener_solicitud(id_).estado)

    def test_solicitud_cerrada_no_admite_cambios_ni_asignaciones(self):
        id_ = self.servicio.registrar(nueva()).id
        self.servicio.cambiar_estado(id_, "CERRADA")
        with self.assertRaises(ErrorDeNegocio):
            self.servicio.cambiar_estado(id_, "NUEVA")
        with self.assertRaises(ErrorDeNegocio):
            self.servicio.asignar_responsable(id_, 1)

    def test_asignar_responsable_inexistente_falla(self):
        id_ = self.servicio.registrar(nueva()).id
        with self.assertRaises(ErrorDeNegocio):
            self.servicio.asignar_responsable(id_, 99)

    def test_buscar_por_texto_ignora_mayusculas(self):
        self.servicio.registrar(nueva(descripcion="Problema con el CAMPUS"))
        self.servicio.registrar(nueva(descripcion="Otra cosa"))
        encontrados = self.servicio.buscar(FiltroSolicitudes.desde_texto(texto="campus"))
        self.assertEqual(1, len(encontrados))

    def test_buscar_combina_filtros(self):
        self.servicio.registrar(nueva(tipo="EQUIVALENCIA"))
        self.servicio.registrar(nueva(tipo="CERTIFICADO"))
        filtro = FiltroSolicitudes.desde_texto(tipo="equivalencia", estado="nueva")
        self.assertEqual(1, len(self.servicio.buscar(filtro)))

    def test_reporte_cuenta_por_estado_y_responsable(self):
        id_ = self.servicio.registrar(nueva()).id
        self.servicio.registrar(nueva())
        self.servicio.asignar_responsable(id_, 1)
        reporte = calcular_reporte(self.repo)
        self.assertEqual(2, reporte.total)
        self.assertEqual(1, reporte.sin_responsable)
        self.assertEqual(1, dict(reporte.por_estado)[Estado.EN_PROCESO])


class PruebasDelRepositorioSqlite(unittest.TestCase):
    def test_los_datos_con_comillas_no_rompen_ni_inyectan_sql(self):
        with tempfile.TemporaryDirectory() as carpeta:
            repo = RepositorioSqlite(os.path.join(carpeta, "t.db"))
            repo.inicializar_con_datos_demo()
            servicio = ServicioSolicitudes(repo)
            id_ = servicio.registrar(nueva(descripcion="Texto con 'comillas'; DROP TABLE solicitudes;--")).id
            self.assertEqual("Texto con 'comillas'; DROP TABLE solicitudes;--",
                             repo.obtener_solicitud(id_).descripcion)
            self.assertEqual(1, len(repo.listar_solicitudes()))


if __name__ == "__main__":
    unittest.main()
