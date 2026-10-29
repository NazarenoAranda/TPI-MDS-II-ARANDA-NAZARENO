import argparse
import os
import sys

from gestor import Gestor


def main():
    p = argparse.ArgumentParser(description="Gestion de Solicitudes Academicas")
    p.add_argument("--db", default="solicitudes.db")
    sp = p.add_subparsers(dest="cmd")
    sp.add_parser("init-demo")
    a = sp.add_parser("registrar")
    a.add_argument("--legajo", required=True)
    a.add_argument("--tipo", required=True)
    a.add_argument("--prioridad", default="MEDIA")
    a.add_argument("--descripcion", required=True)
    b = sp.add_parser("cambiar-estado")
    b.add_argument("--id", type=int, required=True)
    b.add_argument("--estado", required=True)
    c = sp.add_parser("asignar")
    c.add_argument("--id", type=int, required=True)
    c.add_argument("--responsable", type=int, required=True)
    d = sp.add_parser("buscar")
    d.add_argument("--estado")
    d.add_argument("--tipo")
    d.add_argument("--prioridad")
    d.add_argument("--legajo")
    d.add_argument("--texto")
    d.add_argument("--sin-responsable", action="store_true")
    d.add_argument("--responsable", type=int)
    sp.add_parser("reporte")
    args = p.parse_args()

    if args.cmd is None:
        p.print_help()
        return 1

    if args.cmd != "init-demo" and not os.path.exists(args.db):
        print("ERROR: La base de datos no existe. Ejecute primero: init-demo")
        return 1

    g = Gestor(args.db)
    if args.cmd == "init-demo":
        res = g.init()
    elif args.cmd == "registrar":
        res = g.reg(args.legajo, args.tipo, args.prioridad, args.descripcion)
    elif args.cmd == "cambiar-estado":
        res = g.cambiar(args.id, args.estado)
    elif args.cmd == "asignar":
        res = g.asig(args.id, args.responsable)
    elif args.cmd == "buscar":
        res = g.buscar(args.estado, args.tipo, args.prioridad, args.legajo, args.texto, args.sin_responsable, args.responsable)
    elif args.cmd == "reporte":
        res = g.rep()
    print(res)
    if res.startswith("ERROR"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
