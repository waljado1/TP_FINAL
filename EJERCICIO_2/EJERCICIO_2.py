"""
============================================================================
Ejercicio 2 - Modelo de Productos, Excepciones y Persistencia (40 puntos)
EcoTech Solutions - División de Equipamiento Sustentable
============================================================================

"""

import json


# ============================================================================
# DOMINIO DEL CATÁLOGO Y REGLAS DE INVENTARIO
# ============================================================================

# --- Excepción personalizada-------------------------------
class StockInvalidoError(Exception):
    """Lanzada cuando el stock viola las reglas de negocio de EcoTech."""
    pass


# --- Clase Base: DispositivoEcológico-----
class DispositivoEcológico:
    def __init__(self, modelo: str, precio: float, stock: int):
        self.modelo = modelo
        self.precio = precio
        self.set_stock(stock)

    # Getter del atributo privado
    def get_stock(self) -> int:
        return self.__stock

    # Setter con validación de negocio -> dispara StockInvalidoError
    def set_stock(self, nuevo_stock: int):
        
        if nuevo_stock < 0:
            raise StockInvalidoError(
                f"El stock de '{self.modelo}' no puede ser negativo "
                f"(recibido: {nuevo_stock})."
            )
        self.__stock = nuevo_stock

    # Método base que será sobrescrito por las clases hijas (polimorfismo)
    def obtener_ficha_tecnica(self) -> str:
        return f"Modelo: {self.modelo} | Precio: ${self.precio} | Stock: {self.get_stock()}"

    # Patrón DTO: convierte la instancia a un diccionario
    # de tipos primitivos, único formato que json.dump() sabe serializar.
    def a_diccionario(self) -> dict:
        return {
            "modelo": self.modelo,
            "precio": self.precio,
            "stock": self.get_stock()
        }


# --- Clase Especializada: PanelSolar-------------------
class PanelSolar(DispositivoEcológico):
    def __init__(self, modelo: str, precio: float, stock: int,
                 eficiencia_watts: int):
        # Delegamos la inicialización de atributos base a la clase Padre
        super().__init__(modelo, precio, stock)
        # Atributo específico de la clase Hija
        self.eficiencia_watts = eficiencia_watts

    # Polimorfismo: sobrescribimos el método heredado 
    # la ficha técnica con datos propios del panel solar.
    def obtener_ficha_tecnica(self) -> str:
        ficha_base = super().obtener_ficha_tecnica()
        return (f"{ficha_base} | Eficiencia: {self.eficiencia_watts}W "
                f"(Dispositivo de Alta Eficiencia)")

    # El DTO también se sobrescribe para incluir el atributo específico,
    # reutilizando la conversión de la clase base.
    def a_diccionario(self) -> dict:
        datos_base = super().a_diccionario()
        datos_base["eficiencia_watts"] = self.eficiencia_watts
        datos_base["tipo"] = "PanelSolar"
        return datos_base


# ============================================================================
# PERSISTENCIA Y GESTIÓN DEL CATÁLOGO
# ============================================================================

class GestorInventario:
    """Gestor responsable de serializar el catálogo a disco en formato JSON."""

    @staticmethod
    def guardar_catalogo_json(lista_dispositivos: list, ruta_archivo: str) -> None:
        """
        Serializa una lista de DispositivoEcológico a un archivo JSON.
        Cada instancia se convierte previamente a diccionario (DTO) para
        que json.dump() pueda procesarla sin error de tipo.
        """
        # 1. Patrón DTO: transformamos cada objeto en un dict primitivo
        catalogo_serializable = [dispositivo.a_diccionario()
                                 for dispositivo in lista_dispositivos]

        # 2. Serialización a disco: modo "w" sobrescribe el
        # archivo; indent=4 produce un JSON legible; ensure_ascii=False
        # conserva correctamente los acentos del idioma español.
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(catalogo_serializable, archivo, indent=4,
                      ensure_ascii=False)

        print(f"[OK] Catálogo exportado correctamente -> {ruta_archivo}")
        print(f"     Total de dispositivos serializados: {len(catalogo_serializable)}")


# ============================================================================
# BLOQUE DE PRUEBA: 
# ============================================================================

if __name__ == "__main__":

    # --- Intento fallido: stock negativo ---------------------------------
    # Creamos un panel con stock negativo a propósito para verificar que
    # la regla de negocio bloquea la operación y el programa no colapsa.
    print("=" * 70)
    print("PRUEBA 1 - Captura controlada de StockInvalidoError")
    print("=" * 70)

    catalogo = []

    try:
        # Este dispositivo NO debería crearse: stock = -10 viola la regla.
        panel_defectuoso = PanelSolar(
            modelo="SolarMax-Defectuoso",
            precio=1500.0,
            stock=-10,                # <- stock inválido
            eficiencia_watts=450
        )
        catalogo.append(panel_defectuoso)

    except StockInvalidoError as error:
        # Captura controlada (M5 - Clase 2): el programa sigue su curso.
        print(f"[EL STOCK ES NEGATIVO]: {error}")
        print("  -> El stock es inválido fue rechazado y no ingresó al catálogo.\n")

    # --- Construcción del catálogo válido -------------------------------
    print("=" * 70)
    print("PRUEBA 2 - Construcción del catálogo con productos válidos")
    print("=" * 70)

    panel_a = PanelSolar("SolarMax-500", 1500.0, 10, 500)
    panel_b = PanelSolar("SolarPro-300", 980.0, 5, 300)
    panel_c = PanelSolar("EcoPanel-150", 620.0, 8, 150)

    catalogo.extend([panel_a, panel_b, panel_c])

    # Recorremos el catálogo y mostramos la ficha técnica de cada uno.
    # Se evidencia el polimorfismo: aunque todos son PanelSolar, cada uno
    # imprime su propia ficha con sus datos específicos.
    for i, dispositivo in enumerate(catalogo, start=1):
        print(f"  Dispositivo {i}: {dispositivo.obtener_ficha_tecnica()}")
    print()

    # --- Exportación exitosa al archivo JSON ----------------------------
    print("=" * 70)
    print("PRUEBA 3 - Exportación del catálogo a JSON")
    print("=" * 70)

    RUTA_JSON = "catalogo_ecotech.json"
    GestorInventario.guardar_catalogo_json(catalogo, RUTA_JSON)

    # --- Verificación: relectura del archivo generado -------------------
    print("\n" + "=" * 70)
    print("VERIFICACIÓN - Relectura del JSON desde disco")
    print("=" * 70)

    with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
        datos_recuperados = json.load(archivo)

    print(f"Total de ítems cargados desde JSON: {len(datos_recuperados)}")
    for i, item in enumerate(datos_recuperados, start=1):
        print(f"  Ítem {i}: {item}")
