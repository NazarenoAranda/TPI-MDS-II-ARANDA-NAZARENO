"""Interfaz de linea de comandos: traduce argumentos a casos de uso y resultados a texto."""
import argparse
import sys
from typing import List, Optional

from . import presentacion
from .errores import ErrorDeNegocio
from .modelos import FiltroSolicitudes, NuevaSolicitud
from .reporte import calcular_reporte
from .repositorio_sqlite import RepositorioSqlite
from .servicio import ServicioSolicitudes


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gestion de Solicitudes Academicas")
    parser.add_argument("--db", default="solicitudes.db")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("init-demo")

    registrar = sub.add_parser("registrar")
    registrar.add_argument("--legajo", required=True)
    registrar.add_argument("--tipo", required=True)
    registrar.add_argument("--prioridad", default="MEDIA")
    registrar.add_argument("--descripcion", required=True)

    cambiar = sub.add_parser("cambiar-estado")
    cambiar.add_argument("--id", type=int, required=True)
    cambiar.add_argument("--estado", required=True)

    asignar = sub.add_parser("asignar")
    asignar.add_argument("--id", type=int, required=True)
    asignar.add_argument("--responsable", type=int, required=True)

    buscar = sub.add_parser("buscar")
    buscar.add_argument("--estado")
    buscar.add_argument("--tipo")
    buscar.add_argument("--prioridad")
    buscar.add_argument("--legajo")
    buscar.add_argument("--texto")
    buscar.add_argument("--sin-responsable", action="store_true")
    buscar.add_argument("--responsable", type=int)

    sub.add_parser("reporte")
    return parser


def ejecutar(args: argparse.Namespace, repositorio: RepositorioSqlite) -> str:
    """Ejecuta el comando pedido y devuelve el texto a mostrar. Puede lanzar ErrorDeNegocio."""
    servicio = ServicioSolicitudes(repositorio)
    if args.cmd == "init-demo":
        repositorio.inicializar_con_datos_demo()
        return "Base inicializada: 5 estudiantes, 3 responsables."
    if args.cmd == "registrar":
        datos = NuevaSolicitud(args.legajo, args.tipo, args.prioridad, args.descripcion)
        return presentacion.texto_registro(servicio.registrar(datos))
    if args.cmd == "cambiar-estado":
        return presentacion.texto_cambio_estado(servicio.cambiar_estado(args.id, args.estado))
    if args.cmd == "asignar":
        return presentacion.texto_asignacion(servicio.asignar_responsable(args.id, args.responsable))
    if args.cmd == "buscar":
        filtro = FiltroSolicitudes.desde_texto(
            args.estado, args.tipo, args.prioridad, args.legajo, args.texto,
            args.sin_responsable, args.responsable)
        return presentacion.texto_busqueda(servicio.buscar(filtro))
    return presentacion.texto_reporte(calcular_reporte(repositorio))


def main(argv: Optional[List[str]] = None) -> int:
    parser = crear_parser()
    args = parser.parse_args(argv)
    if args.cmd is None:
        parser.print_help()
        return 1

    repositorio = RepositorioSqlite(args.db)
    if args.cmd != "init-demo" and not repositorio.existe():
        print("ERROR: La base de datos no existe. Ejecute primero: init-demo")
        return 1

    try:
        print(ejecutar(args, repositorio))
    except ErrorDeNegocio as error:
        print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
