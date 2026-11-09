Ejercicio 3 - EcoTech Solutions
Auditoría de Algoritmo de Emisiones + Integración Web Django

=== Cómo levantar el proyecto ===

1) Crear y activar entorno virtual:
   python -m venv venv
   venv\Scripts\activate

2) Instalar Django:
   pip install -r requirements.txt

3) Correr los tests:
   python manage.py test sustentabilidad

4) Levantar el servidor:
   python manage.py runserver

5) Abrir en el navegador:
   http://127.0.0.1:8000/sustentabilidad/panel/

=== Estructura ===

EJERCICIO_3/
├── manage.py
├── requirements.txt
├── ecotech/                  -> configuración del proyecto Django
│   ├── settings.py
│   └── urls.py
└── sustentabilidad/          -> app con el ejercicio
    ├── emisiones.py          -> Punto A: función calcular_emisiones_carbono
    ├── tests.py              -> Punto A: clase TestCalculoEmisiones
    ├── views.py              -> Punto B: obtener_metricas_consumo + vista
    ├── urls.py
    └── templates/sustentabilidad/panel.html
