"""Repositorio falso en memoria: permite probar el servicio sin SQLite (gracias a DIP)."""
from solicitudes.modelos import (Estado, Estudiante, NuevaSolicitud, Prioridad, Responsable, Solicitud,
                                 SolicitudDetallada, TipoSolicitud)
from solicitudes.repositorio import RepositorioSolicitudes


class RepositorioEnMemoria(RepositorioSolicitudes):
    def __init__(self):
        self.estudiantes = {"1001": Estudiante("1001", "Ana Perez", "ana@example.com"),
                            "1002": Estudiante("1002", "Bruno Gomez", "bruno@example.com")}
        self.responsables = {1: Responsable(1, "Laura Medina", "Alumnado"),
                             2: Responsable(2, "Martin Sosa", "Equivalencias")}
        self.solicitudes = {}
        self._proximo_id = 1

    def obtener_estudiante(self, legajo):
        return self.estudiantes.get(legajo)

    def obtener_responsable(self, id_responsable):
        return self.responsables.get(id_responsable)

    def listar_responsables(self):
        return sorted(self.responsables.values(), key=lambda r: r.id)

    def obtener_solicitud(self, id_solicitud):
        return self.solicitudes.get(id_solicitud)

    def listar_solicitudes(self):
        detalles = []
        for s in sorted(self.solicitudes.values(), key=lambda x: x.id):
            responsable = self.responsables.get(s.responsable_id)
            detalles.append(SolicitudDetallada(
                s, self.estudiantes[s.legajo].nombre, None if responsable is None else responsable.nombre))
        return detalles

    def guardar_solicitud(self, datos: NuevaSolicitud, tipo: TipoSolicitud, prioridad: Prioridad,
                          descripcion: str, fecha: str) -> int:
        id_nuevo = self._proximo_id
        self._proximo_id += 1
        self.solicitudes[id_nuevo] = Solicitud(id_nuevo, datos.legajo.strip(), tipo, prioridad,
                                               Estado.NUEVA, None, descripcion)
        return id_nuevo

    def actualizar_estado(self, id_solicitud, estado):
        s = self.solicitudes[id_solicitud]
        self.solicitudes[id_solicitud] = Solicitud(s.id, s.legajo, s.tipo, s.prioridad, estado,
                                                   s.responsable_id, s.descripcion)

    def asignar_responsable(self, id_solicitud, id_responsable):
        s = self.solicitudes[id_solicitud]
        self.solicitudes[id_solicitud] = Solicitud(s.id, s.legajo, s.tipo, s.prioridad, s.estado,
                                                   id_responsable, s.descripcion)
