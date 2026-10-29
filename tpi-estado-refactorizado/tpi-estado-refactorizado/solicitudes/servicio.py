"""Casos de uso. Depende de la abstraccion RepositorioSolicitudes, no de SQLite."""
import datetime
from dataclasses import dataclass
from typing import Callable, List, Optional

from .errores import ErrorDeNegocio
from .modelos import (Estado, FiltroSolicitudes, NuevaSolicitud, Prioridad, Responsable, Solicitud,
                      SolicitudDetallada, TipoSolicitud)
from .reglas import ajustar_prioridad, validar_cambio_de_estado, validar_descripcion
from .repositorio import RepositorioSolicitudes


@dataclass(frozen=True)
class ResultadoRegistro:
    id: int
    tipo: TipoSolicitud
    prioridad: Prioridad
    aviso: Optional[str]


@dataclass(frozen=True)
class ResultadoCambioEstado:
    id: int
    estado_anterior: Estado
    estado_nuevo: Estado


@dataclass(frozen=True)
class ResultadoAsignacion:
    id: int
    responsable: Responsable
    paso_a_en_proceso: bool


def _ahora_texto() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class ServicioSolicitudes:
    def __init__(self, repositorio: RepositorioSolicitudes, reloj: Callable[[], str] = _ahora_texto):
        self._repositorio = repositorio
        self._reloj = reloj

    def registrar(self, datos: NuevaSolicitud) -> ResultadoRegistro:
        tipo = TipoSolicitud.desde_texto(datos.tipo)
        prioridad = Prioridad.desde_texto(datos.prioridad)
        descripcion = validar_descripcion(datos.descripcion)
        legajo = datos.legajo.strip()
        self._exigir_estudiante(legajo)
        prioridad_final, aviso = ajustar_prioridad(tipo, prioridad)
        id_nuevo = self._repositorio.guardar_solicitud(datos, tipo, prioridad_final, descripcion, self._reloj())
        return ResultadoRegistro(id_nuevo, tipo, prioridad_final, aviso)

    def cambiar_estado(self, id_solicitud: int, texto_estado: str) -> ResultadoCambioEstado:
        nuevo = Estado.desde_texto(texto_estado)
        solicitud = self._exigir_solicitud(id_solicitud)
        validar_cambio_de_estado(id_solicitud, solicitud.estado, nuevo, solicitud.responsable_id is not None)
        self._repositorio.actualizar_estado(id_solicitud, nuevo)
        return ResultadoCambioEstado(id_solicitud, solicitud.estado, nuevo)

    def asignar_responsable(self, id_solicitud: int, id_responsable: int) -> ResultadoAsignacion:
        solicitud = self._exigir_solicitud(id_solicitud)
        responsable = self._repositorio.obtener_responsable(id_responsable)
        if responsable is None:
            raise ErrorDeNegocio(f"No existe el responsable con id {id_responsable}.")
        if solicitud.estado == Estado.CERRADA:
            raise ErrorDeNegocio(
                f"No se puede asignar responsable a la solicitud #{id_solicitud} porque esta CERRADA.")
        self._repositorio.asignar_responsable(id_solicitud, id_responsable)
        paso_a_en_proceso = solicitud.estado == Estado.NUEVA
        if paso_a_en_proceso:
            self._repositorio.actualizar_estado(id_solicitud, Estado.EN_PROCESO)
        return ResultadoAsignacion(id_solicitud, responsable, paso_a_en_proceso)

    def buscar(self, filtro: FiltroSolicitudes) -> List[SolicitudDetallada]:
        return [d for d in self._repositorio.listar_solicitudes() if filtro.coincide(d)]

    def _exigir_estudiante(self, legajo: str) -> None:
        if self._repositorio.obtener_estudiante(legajo) is None:
            raise ErrorDeNegocio(f"No existe el estudiante con legajo '{legajo}'.")

    def _exigir_solicitud(self, id_solicitud: int) -> Solicitud:
        solicitud = self._repositorio.obtener_solicitud(id_solicitud)
        if solicitud is None:
            raise ErrorDeNegocio(f"No existe la solicitud #{id_solicitud}.")
        return solicitud
