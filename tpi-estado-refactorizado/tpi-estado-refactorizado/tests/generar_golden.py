"""Regenera los archivos golden a partir del sistema actual.

IMPORTANTE: los golden files oficiales de este TPI se generaron con la version
INICIAL (tag estado-inicial); no regenerar con la versión refactorizada. No se deben regenerar con la version refactorizada,
porque entonces la prueba no demostraria nada.

Uso (desde la raiz del proyecto):  python tests/generar_golden.py
"""
from ayuda_golden import ejecutar_escenario, escribir_golden
from escenarios import ESCENARIOS

if __name__ == "__main__":
    for nombre, comandos in ESCENARIOS.items():
        escribir_golden(nombre, ejecutar_escenario(comandos))
        print("golden generado:", nombre)
