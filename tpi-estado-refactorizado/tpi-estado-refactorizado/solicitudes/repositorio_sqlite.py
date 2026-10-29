"""Implementacion SQLite del repositorio. Todas las consultas usan parametros (sin concatenar SQL)."""
import os
import sqlite3
from contextlib import contextmanager
from typing import List, Optional

from .modelos import (Estado, Estudiante, NuevaSolicitud, Prioridad, Responsable, Solicitud,
                      SolicitudDetallada, TipoSolicitud)
from .repositorio import RepositorioSolicitudes

ESQUEMA = (
    "CREATE TABLE estudiantes (legajo TEXT PRIMARY KEY, nombre TEXT, email TEXT)",
    "CREATE TABLE responsables (id INTEGER PRIMARY KEY, nombre TEXT, area TEXT)",
    "CREATE TABLE solicitudes (id INTEGER PRIMARY KEY AUTOINCREMENT, legajo TEXT, tipo TEXT, "
    "prioridad TEXT, estado TEXT, responsable_id INTEGER, descripcion TEXT, canal TEXT, "
    "creado_por TEXT, fecha TEXT)",
)

# Datos sinteticos (el TPI prohibe datos personales reales).
ESTUDIANTES_DEMO = (
    ("1001", "Ana Perez", "ana.perez@example.com"),
    ("1002", "Bruno Gomez", "bruno.gomez@example.com"),
    ("1003", "Carla Diaz", "carla.diaz@example.com"),
    ("1004", "Diego Torres", "diego.torres@example.com"),
    ("1005", "Elena Ruiz", "elena.ruiz@example.com"),
)
RESPONSABLES_DEMO = (
    (1, "Laura Medina", "Alumnado"),
    (2, "Martin Sosa", "Equivalencias"),
    (3, "Julia Ferrari", "Bedelia"),
)

CONSULTA_DETALLE = (
    "SELECT s.id, s.legajo, s.tipo, s.prioridad, s.estado, s.responsable_id, s.descripcion, "
    "e.nombre, r.nombre "
    "FROM solicitudes s "
    "LEFT JOIN estudiantes e ON e.legajo = s.legajo "
    "LEFT JOIN responsables r ON r.id = s.responsable_id "
    "ORDER BY s.id"
)


def _a_solicitud(fila) -> Solicitud:
    return Solicitud(
        id=fila[0], legajo=fila[1], tipo=TipoSolicitud(fila[2]), prioridad=Prioridad(fila[3]),
        estado=Estado(fila[4]), responsable_id=fila[5], descripcion=fila[6])


class RepositorioSqlite(RepositorioSolicitudes):
    def __init__(self, ruta_db: str):
        self._ruta_db = ruta_db

    def existe(self) -> bool:
        return os.path.exists(self._ruta_db)

    def inicializar_con_datos_demo(self) -> None:
        if self.existe():
            os.remove(self._ruta_db)
        with self._conexion() as conexion:
            for sentencia in ESQUEMA:
                conexion.execute(sentencia)
            conexion.executemany("INSERT INTO estudiantes VALUES (?, ?, ?)", ESTUDIANTES_DEMO)
            conexion.executemany("INSERT INTO responsables VALUES (?, ?, ?)", RESPONSABLES_DEMO)

    @contextmanager
    def _conexion(self):
        """Conexion que hace commit/rollback y se cierra al salir del bloque `with`."""
        conexion = sqlite3.connect(self._ruta_db)
        try:
            yield conexion
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def obtener_estudiante(self, legajo: str) -> Optional[Estudiante]:
        with self._conexion() as c:
            fila = c.execute("SELECT legajo, nombre, email FROM estudiantes WHERE legajo = ?", (legajo,)).fetchone()
        return None if fila is None else Estudiante(*fila)

    def obtener_responsable(self, id_responsable: int) -> Optional[Responsable]:
        with self._conexion() as c:
            fila = c.execute("SELECT id, nombre, area FROM responsables WHERE id = ?", (id_responsable,)).fetchone()
        return None if fila is None else Responsable(*fila)

    def listar_responsables(self) -> List[Responsable]:
        with self._conexion() as c:
            filas = c.execute("SELECT id, nombre, area FROM responsables ORDER BY id").fetchall()
        return [Responsable(*fila) for fila in filas]

    def obtener_solicitud(self, id_solicitud: int) -> Optional[Solicitud]:
        with self._conexion() as c:
            fila = c.execute(
                "SELECT id, legajo, tipo, prioridad, estado, responsable_id, descripcion "
                "FROM solicitudes WHERE id = ?", (id_solicitud,)).fetchone()
        return None if fila is None else _a_solicitud(fila)

    def listar_solicitudes(self) -> List[SolicitudDetallada]:
        with self._conexion() as c:
            filas = c.execute(CONSULTA_DETALLE).fetchall()
        return [SolicitudDetallada(_a_solicitud(f), f[7], f[8]) for f in filas]

    def guardar_solicitud(self, datos: NuevaSolicitud, tipo: TipoSolicitud, prioridad: Prioridad,
                          descripcion: str, fecha: str) -> int:
        with self._conexion() as c:
            cursor = c.execute(
                "INSERT INTO solicitudes (legajo, tipo, prioridad, estado, responsable_id, descripcion, "
                "canal, creado_por, fecha) VALUES (?, ?, ?, ?, NULL, ?, ?, ?, ?)",
                (datos.legajo.strip(), tipo.value, prioridad.value, Estado.NUEVA.value, descripcion,
                 datos.canal, datos.creado_por, fecha))
            return cursor.lastrowid

    def actualizar_estado(self, id_solicitud: int, estado: Estado) -> None:
        with self._conexion() as c:
            c.execute("UPDATE solicitudes SET estado = ? WHERE id = ?", (estado.value, id_solicitud))

    def asignar_responsable(self, id_solicitud: int, id_responsable: int) -> None:
        with self._conexion() as c:
            c.execute("UPDATE solicitudes SET responsable_id = ? WHERE id = ?", (id_responsable, id_solicitud))
