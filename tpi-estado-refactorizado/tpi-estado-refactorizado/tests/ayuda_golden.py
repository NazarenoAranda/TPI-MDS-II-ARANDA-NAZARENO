"""Ayudas para las pruebas de caracterizacion ("golden master")."""
import os
import shlex
import subprocess
import sys
import tempfile

from escenarios import ESCENARIOS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_GOLDEN = os.path.join(RAIZ, "tests", "golden")


def ejecutar_escenario(comandos):
    """Ejecuta los comandos en orden y devuelve la transcripcion completa."""
    entorno = dict(os.environ, PYTHONIOENCODING="utf-8")
    with tempfile.TemporaryDirectory() as carpeta_temporal:
        ruta_db = os.path.join(carpeta_temporal, "prueba.db")
        partes = []
        for argumentos in comandos:
            resultado = subprocess.run(
                [sys.executable, "main.py", "--db", ruta_db] + argumentos,
                cwd=RAIZ,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=entorno,
            )
            partes.append(
                "$ " + shlex.join(argumentos) + "\n"
                + resultado.stdout
                + "[exit " + str(resultado.returncode) + "]\n"
            )
        return "\n".join(partes)


def ruta_golden(nombre):
    return os.path.join(CARPETA_GOLDEN, nombre + ".txt")


def leer_golden(nombre):
    with open(ruta_golden(nombre), encoding="utf-8") as archivo:
        return archivo.read()


def escribir_golden(nombre, contenido):
    os.makedirs(CARPETA_GOLDEN, exist_ok=True)
    with open(ruta_golden(nombre), "w", encoding="utf-8", newline="\n") as archivo:
        archivo.write(contenido)


def nombres_escenarios():
    return list(ESCENARIOS.keys())
