"""Tests unitarios del algoritmo de emisiones (Punto A).

Cubre dos frentes:
  - exactitud numérica con valores nominales (consumos válidos)
  - correcta elevación de ValueError ante consumos fuera de rango
"""
import unittest

from .emisiones import calcular_emisiones_carbono


class TestCalculoEmisiones(unittest.TestCase):
    """Auditoría de calcular_emisiones_carbono."""

    # --- Exactitud numérica: valores nominales -----------------------------

    def test_calculo_consumo_normal(self):
        # Caso típico: 100 kWh con factor 0.4 -> 40 kg de CO2
        resultado = calcular_emisiones_carbono(100)
        self.assertEqual(resultado, 40.0)

    def test_calculo_consumo_cero(self):
        # Consumo 0 es un valor límite válido: no debe romper, devuelve 0
        self.assertEqual(calcular_emisiones_carbono(0), 0.0)

    def test_factor_emision_personalizado(self):
        # Si paso otro factor, la función lo respeta
        self.assertEqual(calcular_emisiones_carbono(100, 0.5), 50.0)

    def test_volumen_industrial(self):
        # Consumo alto, típico de una planta: 12000 kWh -> 4800 kg
        self.assertEqual(calcular_emisiones_carbono(12000), 4800.0)

    def test_consumo_decimal(self):
        # Consumo con decimales: uso assertAlmostEqual por el punto flotante
        self.assertAlmostEqual(calcular_emisiones_carbono(250.5), 100.2)

    # --- Excepción: consumos fuera de rango -------------------------------

    def test_consumo_negativo_lanza_value_error(self):
        # Consumo negativo: tiene que elevar ValueError
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-50)

    def test_consumo_negativo_chico_lanza_value_error(self):
        # Incluso un negativo chico debe lanzar la excepción
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-0.1)
