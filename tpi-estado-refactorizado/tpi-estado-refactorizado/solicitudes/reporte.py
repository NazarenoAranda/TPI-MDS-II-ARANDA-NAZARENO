"""Calculo del reporte (datos) separado de su presentacion (texto)."""
from collections import Counter
from dataclasses import dataclass
from typing import List, Tuple

from .modelos import Estado, Prioridad, Responsable, TipoSolicitud
from .repositorio import RepositorioSolicitudes

# El orden de prioridades en el reporte es de mayor a menor (distinto al orden del enum).
ORDEN_PRIORIDADES_REPORTE = (Prioridad.ALTA, Prioridad.MEDIA, Prioridad.BAJA)


@dataclass(frozen=True)
class DatosReporte:
    total: int
    sin_responsable: int
    por_estado: List[Tuple[Estado, int]]
    por_tipo: List[Tuple[TipoSolicitud, int]]
    por_prioridad: List[Tuple[Prioridad, int]]
    por_responsable: List[Tuple[Responsable, int]]


def calcular_reporte(repositorio: RepositorioSolicitudes) -> DatosReporte:
    solicitudes = [d.solicitud for d in repositorio.listar_solicitudes()]
    por_estado = Counter(s.estado for s in solicitudes)
    por_tipo = Counter(s.tipo for s in solicitudes)
    por_prioridad = Counter(s.prioridad for s in solicitudes)
    por_responsable = Counter(s.responsable_id for s in solicitudes)
    return DatosReporte(
        total=len(solicitudes),
        sin_responsable=por_responsable[None],
        por_estado=[(e, por_estado[e]) for e in Estado],
        por_tipo=[(t, por_tipo[t]) for t in TipoSolicitud],
        por_prioridad=[(p, por_prioridad[p]) for p in ORDEN_PRIORIDADES_REPORTE],
        por_responsable=[(r, por_responsable[r.id]) for r in repositorio.listar_responsables()],
    )
