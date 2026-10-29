"""Entidades, enumeraciones y objetos de parametros del dominio (sin dependencias de infraestructura)."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type, TypeVar

from .errores import ErrorDeNegocio

LONGITUD_MAXIMA_DESCRIPCION = 200

E = TypeVar("E", bound=Enum)


def _parsear(clase_enum: Type[E], texto: str, nombre_invalido: str) -> E:
    """Convierte texto del usuario en un miembro del enum (sin distinguir mayusculas ni espacios)."""
    normalizado = texto.upper().strip()
    for miembro in clase_enum:
        if miembro.value == normalizado:
            return miembro
    validos = ", ".join(miembro.value for miembro in clase_enum)
    raise ErrorDeNegocio(f"{nombre_invalido} '{normalizado}'. Valores validos: {validos}.")


class TipoSolicitud(Enum):
    CERTIFICADO = "CERTIFICADO"
    EQUIVALENCIA = "EQUIVALENCIA"
    REINCORPORACION = "REINCORPORACION"
    CONSULTA = "CONSULTA"

    @property
    def plazo_estimado_dias(self) -> int:
        return _PLAZOS_ESTIMADOS_DIAS[self]

    @classmethod
    def desde_texto(cls, texto: str) -> "TipoSolicitud":
        return _parsear(cls, texto, "Tipo invalido")


_PLAZOS_ESTIMADOS_DIAS = {
    TipoSolicitud.CERTIFICADO: 5,
    TipoSolicitud.EQUIVALENCIA: 15,
    TipoSolicitud.REINCORPORACION: 10,
    TipoSolicitud.CONSULTA: 3,
}


class Prioridad(Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"

    @classmethod
    def desde_texto(cls, texto: str) -> "Prioridad":
        return _parsear(cls, texto, "Prioridad invalida")


class Estado(Enum):
    NUEVA = "NUEVA"
    EN_PROCESO = "EN_PROCESO"
    RESUELTA = "RESUELTA"
    CERRADA = "CERRADA"

    @classmethod
    def desde_texto(cls, texto: str) -> "Estado":
        return _parsear(cls, texto, "Estado invalido")


@dataclass(frozen=True)
class Estudiante:
    legajo: str
    nombre: str
    email: str


@dataclass(frozen=True)
class Responsable:
    id: int
    nombre: str
    area: str


@dataclass(frozen=True)
class Solicitud:
    id: int
    legajo: str
    tipo: TipoSolicitud
    prioridad: Prioridad
    estado: Estado
    responsable_id: Optional[int]
    descripcion: str


@dataclass(frozen=True)
class SolicitudDetallada:
    """Solicitud junto con los nombres que se muestran en listados."""
    solicitud: Solicitud
    nombre_estudiante: str
    nombre_responsable: Optional[str]


@dataclass(frozen=True)
class NuevaSolicitud:
    """Parameter Object: agrupa los datos de entrada para registrar una solicitud."""
    legajo: str
    tipo: str
    prioridad: str
    descripcion: str
    canal: str = "CLI"
    creado_por: str = "sistema"


@dataclass(frozen=True)
class FiltroSolicitudes:
    """Parameter Object: criterios opcionales de busqueda. Un criterio en None no filtra."""
    estado: Optional[Estado] = None
    tipo: Optional[TipoSolicitud] = None
    prioridad: Optional[Prioridad] = None
    legajo: Optional[str] = None
    texto: Optional[str] = None
    solo_sin_responsable: bool = False
    responsable_id: Optional[int] = None

    @classmethod
    def desde_texto(cls, estado=None, tipo=None, prioridad=None, legajo=None, texto=None,
                    solo_sin_responsable=False, responsable_id=None) -> "FiltroSolicitudes":
        """Construye el filtro validando los textos ingresados por el usuario (en el orden estado, tipo, prioridad)."""
        return cls(
            estado=None if estado is None else Estado.desde_texto(estado),
            tipo=None if tipo is None else TipoSolicitud.desde_texto(tipo),
            prioridad=None if prioridad is None else Prioridad.desde_texto(prioridad),
            legajo=None if legajo is None else legajo.strip(),
            texto=texto,
            solo_sin_responsable=solo_sin_responsable,
            responsable_id=responsable_id,
        )

    def coincide(self, detalle: SolicitudDetallada) -> bool:
        """Move Method: la logica de filtrado vive junto a los datos del filtro."""
        s = detalle.solicitud
        if self.estado is not None and s.estado != self.estado:
            return False
        if self.tipo is not None and s.tipo != self.tipo:
            return False
        if self.prioridad is not None and s.prioridad != self.prioridad:
            return False
        if self.legajo is not None and s.legajo != self.legajo:
            return False
        if self.texto is not None and self.texto.lower() not in s.descripcion.lower():
            return False
        if self.solo_sin_responsable and s.responsable_id is not None:
            return False
        if self.responsable_id is not None and s.responsable_id != self.responsable_id:
            return False
        return True
