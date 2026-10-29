"""Pruebas de caracterizacion: la salida del sistema debe coincidir con los golden files."""
import unittest

from ayuda_golden import ejecutar_escenario, leer_golden
from escenarios import ESCENARIOS


class PruebasDeCaracterizacion(unittest.TestCase):
    def comparar(self, nombre):
        obtenido = ejecutar_escenario(ESCENARIOS[nombre])
        esperado = leer_golden(nombre)
        self.assertEqual(esperado, obtenido, "La salida del escenario '" + nombre + "' cambio")

    def test_flujo_completo(self):
        self.comparar("flujo_completo")

    def test_errores_de_negocio(self):
        self.comparar("errores")

    def test_sin_base_de_datos(self):
        self.comparar("sin_base")


if __name__ == "__main__":
    unittest.main()
