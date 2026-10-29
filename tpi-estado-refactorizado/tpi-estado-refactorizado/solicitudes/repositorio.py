"""Puerto de persistencia (abstraccion) del que depende el servicio: Dependency Inversion."""
from abc import ABC, abstractmethod
from typing import List, Optional

from .modelos import (Estado, Estudiante, NuevaSolicitud, Prioridad, Responsable, Solicitud,
                      SolicitudDetallada, TipoSolicitud)


class RepositorioSolicitudes(ABC):
    @abstractmethod
    def obtener_estudiante(self, legajo: str) -> Optional[Estudiante]: ...

    @abstractmethod
    def obtener_responsable(self, id_responsable: int) -> Optional[Responsable]: ...

    @abstractmethod
    def listar_responsables(self) -> List[Responsable]: ...

    @abstractmethod
    def obtener_solicitud(self, id_solicitud: int) -> Optional[Solicitud]: ...

    @abstractmethod
    def listar_solicitudes(self) -> List[SolicitudDetallada]: ...

    @abstractmethod
    def guardar_solicitud(self, datos: NuevaSolicitud, tipo: TipoSolicitud, prioridad: Prioridad,
                          descripcion: str, fecha: str) -> int: ...

    @abstractmethod
    def actualizar_estado(self, id_solicitud: int, estado: Estado) -> None: ...

    @abstractmethod
    def asignar_responsable(self, id_solicitud: int, id_responsable: int) -> None: ...
