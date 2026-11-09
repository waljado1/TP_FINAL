"""Vistas de la app sustentabilidad (Punto B)."""
from django.shortcuts import render

from .emisiones import calcular_emisiones_carbono


# Historial de consumos por planta industrial.
# En un sistema real vendría de una consulta al ORM, pero para este
# ejercicio lo dejo como lista de diccionarios.
REGISTROS = [
    {"planta": "Planta Norte",  "consumo_kwh": 12000},
    {"planta": "Planta Sur",    "consumo_kwh": 8500},
    {"planta": "Planta Centro", "consumo_kwh": 15300},
    {"planta": "Planta Oeste",  "consumo_kwh": 6700},
]


def obtener_metricas_consumo(registros):
    """Recorre el historial de consumos por planta y calcula:

      - el total global de emisiones (sumando las emisiones de cada planta)
      - la planta con mayor consumo
      - un detalle por planta para mostrar en la tabla del panel

    Usa calcular_emisiones_carbono (del Punto A) para obtener las
    emisiones de cada planta a partir de su consumo.
    """
    total_emisiones = 0
    total_consumo = 0
    planta_mayor = None
    consumo_mayor = -1
    detalle = []

    for registro in registros:
        consumo = registro["consumo_kwh"]
        # Acá incorporo la función auditada en el Punto A
        emisiones = calcular_emisiones_carbono(consumo)

        total_emisiones += emisiones
        total_consumo += consumo

        # Me quedo con la planta de mayor consumo
        if consumo > consumo_mayor:
            consumo_mayor = consumo
            planta_mayor = registro["planta"]

        detalle.append({
            "planta": registro["planta"],
            "consumo_kwh": consumo,
            "emisiones_kg": emisiones,
        })

    return {
        "total_emisiones": total_emisiones,
        "total_consumo_kwh": total_consumo,
        "planta_mayor_consumo": planta_mayor,
        "consumo_mayor_kwh": consumo_mayor,
        "cantidad_plantas": len(registros),
        "detalle": detalle,
    }


def vista_panel_sustentabilidad(request):
    """Vista del panel de sustentabilidad.

    Procesa las métricas de consumo y le pasa el contexto a la plantilla
    sustentabilidad/panel.html para que la renderice.
    """
    metricas = obtener_metricas_consumo(REGISTROS)

    contexto = {
        "titulo": "Panel de Sustentabilidad - EcoTech Solutions",
        "metricas": metricas,
        "registros": metricas["detalle"],
        "factor_emision": 0.4,
    }
    return render(request, "sustentabilidad/panel.html", contexto)
