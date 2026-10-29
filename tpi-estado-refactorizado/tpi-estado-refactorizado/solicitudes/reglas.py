"""Reglas de negocio expresadas como datos/funciones pequenas (abiertas a extension, OCP)."""
from dataclasses import dataclass
from typing import Optional, Tuple

from .errores import ErrorDeNegocio
from .modelos import Estado, LONGITUD_MAXIMA_DESCRIPCION, Prioridad, TipoSolicitud


@dataclass(frozen=True)
class ReglaDePrioridad:
    """Si una solicitud de `tipo` llega con prioridad `desde`, se cambia a `hacia` y se avisa."""
    tipo: TipoSolicitud
    desde: Prioridad
    hacia: Prioridad
    aviso: str


# Para agregar una regla nueva alcanza con sumar una entrada: no hay que tocar el servicio.
REGLAS_DE_PRIORIDAD = (
    ReglaDePrioridad(TipoSolicitud.REINCORPORACION, Prioridad.BAJA, Prioridad.MEDIA,
                     "Aviso: prioridad elevada a MEDIA por tipo REINCORPORACION."),
    ReglaDePrioridad(TipoSolicitud.CONSULTA, Prioridad.ALTA, Prioridad.MEDIA,
                     "Aviso: prioridad reducida a MEDIA por tipo CONSULTA."),
)

ESTADOS_QUE_EXIGEN_RESPONSABLE = (Estado.EN_PROCESO, Estado.RESUELTA)


def ajustar_prioridad(tipo: TipoSolicitud, prioridad: Prioridad) -> Tuple[Prioridad, Optional[str]]:
    """Devuelve la prioridad final y, si hubo ajuste, el aviso para el usuario."""
    for regla in REGLAS_DE_PRIORIDAD:
        if regla.tipo == tipo and regla.desde == prioridad:
            return regla.hacia, regla.aviso
    return prioridad, None


def validar_descripcion(descripcion: str) -> str:
    """Devuelve la descripcion sin espacios sobrantes o lanza ErrorDeNegocio."""
    limpia = descripcion.strip()
    if len(limpia) == 0:
        raise ErrorDeNegocio("La descripcion no puede estar vacia.")
    if len(limpia) > LONGITUD_MAXIMA_DESCRIPCION:
        raise ErrorDeNegocio(f"La descripcion supera los {LONGITUD_MAXIMA_DESCRIPCION} caracteres.")
    return limpia


def validar_cambio_de_estado(id_solicitud: int, actual: Estado, nuevo: Estado, tiene_responsable: bool) -> None:
    """Lanza ErrorDeNegocio si la transicion `actual -> nuevo` no esta permitida."""
    if actual == Estado.CERRADA:
        raise ErrorDeNegocio(f"La solicitud #{id_solicitud} esta CERRADA y no admite cambios de estado.")
    if actual == nuevo:
        raise ErrorDeNegocio(f"La solicitud #{id_solicitud} ya esta en estado {nuevo.value}.")
    if nuevo in ESTADOS_QUE_EXIGEN_RESPONSABLE and not tiene_responsable:
        raise ErrorDeNegocio(
            f"La solicitud #{id_solicitud} necesita un responsable antes de pasar a {nuevo.value}.")
