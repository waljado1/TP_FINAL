"""
Normalización y filtrado de sensores
====================================
1) limpiar_registro_sensor(registro_raw)
   Normaliza un diccionario crudo de sensor (limpia espacios, quita sufijos
   de unidad, asigna valores por defecto seguros).

2) Filtrado de sensores en alerta
   Pide un umbral de temperatura por teclado (input()) y filtra los sensores
   que lo superan usando filter() + lambda. Extrae los IDs con map() + lambda.

3) Cálculo de promedios
   Calcula el promedio general de los sensores con temperatura válida.

Los datos corruptos están declarados DENTRO del código como una lista de
diccionarios.
"""


# =========================================================================
# FUNCIÓN DE NORMALIZACIÓN
# =========================================================================
def limpiar_registro_sensor(registro_raw: dict) -> dict:
    """
    Procesa un diccionario con datos crudos de un sensor y retorna un
    diccionario estandarizado con los campos limpios y tipados.

    Transformaciones:
      - sensor_id   : .strip() elimina espacios/tabs/saltos sobrantes.
                      Si falta o está vacío, se asigna "ID desconocido".
      - temperatura : se quitan sufijos ('C', '°C', 'ºC', 'c') y se
                      convierte a float. Si falta, se asigna "NO REGISTRADA".
      - ubicacion   : si falta, es None o solo tiene espacios, se asigna
                      el valor por defecto "No registrada".
    """
    # 1. Limpieza de sensor_id
    sensor_id = str(registro_raw.get("sensor_id", "ID desconocido")).strip()
    if sensor_id == "":
        sensor_id = "ID desconocido"

    # 2. Limpieza y conversión de temperatura
    temp_raw = registro_raw.get("temperatura")
    if temp_raw is None:
        temperatura = "NO REGISTRADA"
    else:
        temp_str = str(temp_raw).strip()
        for sufijo in ("°C", "°c", "ºC", "ºc", "C", "c", "°", "º"):
            temp_str = temp_str.replace(sufijo, "")
        temp_str = temp_str.strip()
        try:
            temperatura = float(temp_str)
        except ValueError:
            raise ValueError(
                f"No se pudo convertir la temperatura a float: '{temp_raw}'"
            )

    # 3. Ubicación con valor por defecto seguro
    ubicacion_raw = registro_raw.get("ubicacion")
    if ubicacion_raw is None or str(ubicacion_raw).strip() == "":
        ubicacion = "No registrada"
    else:
        ubicacion = str(ubicacion_raw).strip()

    # 4. Retorno del diccionario estandarizado
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion,
    }


# =========================================================================
# DATOS CORRUPTOS DENTRO DEL CÓDIGO (lista de diccionarios)
# =========================================================================

registros_corruptos = [
    {
        "sensor_id": " SENSOR-001 ",
        "temperatura": "24.5C",
        "ubicacion": "Planta Norte",
    },
    {
        "sensor_id": "  SENSOR-002  ",
        "temperatura": "  31.2°C  ",
        "ubicacion": "Planta Sur",
    },
    {
        "sensor_id": "SENSOR-003",
        "temperatura": " 28.0 C ",
        "ubicacion": "",
    },
    {
        "sensor_id": "   SENSOR-004   ",
        "temperatura": "29.5°C",
    },
    {
        "sensor_id": " SENSOR-005 ",
        "temperatura": " 22.1c ",
        "ubicacion": "   ",
    },
    {
        "sensor_id": "",
        "temperatura": "\n25.0C\n",
        "ubicacion": "Planta Este",
    },
    {
        "sensor_id": "SENSOR-007",
        "temperatura": 27,
        "ubicacion": "  Planta Oeste  ",
    },
    {
        "sensor_id": " SENSOR-008 ",
        "ubicacion": "Planta Centro",
    },
]


# =========================================================================
# LÓGICA PRINCIPAL
# =========================================================================
def main():
    # 1. Normalizamos todos los registros corruptos
    sensores = [limpiar_registro_sensor(r) for r in registros_corruptos]

    print("=" * 70)
    print("Normalización y filtrado de sensores")
    print("=" * 70)

    # Mostramos los registros normalizados
    print("\nRegistros normalizados:")
    for s in sensores:
        temp_str = (
            f"{s['temperatura']:>5} °C"
            if isinstance(s["temperatura"], float)
            else f"{s['temperatura']:>14}"
        )
        print(f"  {s['sensor_id']:>16}  |  {temp_str}  |  {s['ubicacion']}")

    # 2. Pedimos el umbral por teclado con input()
    print("\n" + "-" * 70)
    print("Filtrado de sensores en alerta")
    print("-" * 70)
    while True:
        umbral_input = input("Ingrese el umbral de temperatura (°C): ").strip()
        try:
            umbral = float(umbral_input)
            break
        except ValueError:
            print("  [!] Valor inválido. Ingrese un número, por ejemplo: 25.0")

    print(f"\nUmbral configurado por el usuario: {umbral} °C")
    print("-" * 70)

    # 3. Separar sensores con temperatura válida de los que no la tienen
    sensores_con_temp = list(
        filter(lambda s: isinstance(s["temperatura"], float), sensores)
    )
    sensores_sin_temp = list(
        filter(lambda s: not isinstance(s["temperatura"], float), sensores)
    )

    # 4. Filtrado con filter() + lambda (solo sobre los que tienen temperatura)
    sensores_alerta = list(
        filter(lambda s: s["temperatura"] > umbral, sensores_con_temp)
    )
    sensores_ok = list(filter(lambda s: s["temperatura"] <= umbral, sensores_con_temp))

    # 5. Extracción de IDs con map() + lambda
    ids_alerta = list(map(lambda s: s["sensor_id"], sensores_alerta))

    # 6. Reporte por consola
    print(f"\n>>> Sensores EN ALERTA (temp > {umbral} °C): {len(sensores_alerta)}")
    if sensores_alerta:
        for s in sensores_alerta:
            print(
                f"    - {s['sensor_id']:>16}  |  {s['temperatura']:>5} °C  |  {s['ubicacion']}"
            )
        print(f"\n    IDs en alerta: {ids_alerta}")
    else:
        print("    (ningún sensor supera el umbral)")

    print(f"\n>>> Sensores OK (temp <= {umbral} °C): {len(sensores_ok)}")
    for s in sensores_ok:
        print(
            f"    - {s['sensor_id']:>16}  |  {s['temperatura']:>5} °C  |  {s['ubicacion']}"
        )

    if sensores_sin_temp:
        print(f"\n>>> Sensores SIN TEMPERATURA REGISTRADA: {len(sensores_sin_temp)}")
        for s in sensores_sin_temp:
            print(
                f"    - {s['sensor_id']:>16}  |  {s['temperatura']:>14}  |  {s['ubicacion']}"
            )

    # 7. Cálculo del promedio general (solo sensores con temperatura válida)
    print("\n" + "-" * 70)
    print("Promedio de temperaturas")
    print("-" * 70)

    if sensores_con_temp:
        promedio_general = sum(s["temperatura"] for s in sensores_con_temp) / len(
            sensores_con_temp
        )
        print(
            f"\nPromedio general ({len(sensores_con_temp)} sensores con temperatura): {promedio_general:.2f} °C"
        )
    else:
        print("\nNo hay sensores con temperatura válida para calcular el promedio.")


if __name__ == "__main__":
    main()
