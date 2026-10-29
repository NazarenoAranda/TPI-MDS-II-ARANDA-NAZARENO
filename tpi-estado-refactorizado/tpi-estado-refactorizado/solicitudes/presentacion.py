"""Formateo de resultados a texto. Es lo unico que conoce el formato de salida por consola."""
from typing import List

from .reporte import DatosReporte
from .modelos import SolicitudDetallada
from .servicio import ResultadoAsignacion, ResultadoCambioEstado, ResultadoRegistro


def texto_registro(r: ResultadoRegistro) -> str:
    linea = f"Solicitud #{r.id} registrada ({r.tipo.value}, prioridad {r.prioridad.value}, estado NUEVA)."
    return linea if r.aviso is None else r.aviso + "\n" + linea


def texto_cambio_estado(r: ResultadoCambioEstado) -> str:
    return f"Solicitud #{r.id}: estado {r.estado_anterior.value} -> {r.estado_nuevo.value}."


def texto_asignacion(r: ResultadoAsignacion) -> str:
    texto = f"Solicitud #{r.id} asignada a {r.responsable.nombre} ({r.responsable.area})."
    if r.paso_a_en_proceso:
        texto += f"\nSolicitud #{r.id} paso automaticamente a EN_PROCESO."
    return texto


def texto_busqueda(resultados: List[SolicitudDetallada]) -> str:
    if not resultados:
        return "No se encontraron solicitudes."
    lineas = [_linea_solicitud(d) for d in resultados]
    return "\n".join(lineas) + f"\nTotal: {len(resultados)} solicitud(es)"


def _linea_solicitud(d: SolicitudDetallada) -> str:
    s = d.solicitud
    responsable = d.nombre_responsable if d.nombre_responsable is not None else "sin asignar"
    return (f"#{s.id} | {s.tipo.value} | {s.prioridad.value} | {s.estado.value} | "
            f"{s.legajo} {d.nombre_estudiante} | {responsable} | {s.descripcion}")


def texto_reporte(datos: DatosReporte) -> str:
    lineas = [
        "=== REPORTE DE SOLICITUDES ===",
        f"Total de solicitudes: {datos.total}",
        f"Sin responsable asignado: {datos.sin_responsable}",
        "",
        "Por estado:",
        *[f"  {estado.value}: {cantidad}" for estado, cantidad in datos.por_estado],
        "",
        "Por tipo:",
        *[f"  {tipo.value}: {cantidad} (plazo estimado: {tipo.plazo_estimado_dias} dias)"
          for tipo, cantidad in datos.por_tipo],
        "",
        "Por prioridad:",
        *[f"  {prioridad.value}: {cantidad}" for prioridad, cantidad in datos.por_prioridad],
        "",
        "Carga por responsable:",
        *[f"  {r.nombre} ({r.area}): {cantidad}" for r, cantidad in datos.por_responsable],
    ]
    return "\n".join(lineas)
