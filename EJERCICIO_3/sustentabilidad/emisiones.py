"""Algoritmo de cálculo de emisiones de carbono para EcoTech Solutions."""


def calcular_emisiones_carbono(consumo_kwh: float, factor_emision: float = 0.4) -> float:
    """Calcula las emisiones de CO2 (kg) a partir del consumo eléctrico (kWh).

    Por defecto usa el factor 0.4 kg CO2/kWh. Lanza ValueError si el
    consumo es negativo, porque no tiene sentido físico.
    """
    if consumo_kwh < 0:
        raise ValueError("El consumo energético no puede ser negativo.")
    return consumo_kwh * factor_emision
