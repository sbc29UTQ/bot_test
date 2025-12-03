"""
Archivo de configuración de ejemplo para el scraper de LinkedIn
Copia este archivo a config.py y personaliza según tus necesidades
"""

# Configuración de búsqueda
SEARCH_CONFIG = {
    # Keywords para buscar perfiles de LinkedIn
    "keywords": [
        "python developer",
        "data scientist",
        "machine learning engineer"
    ],

    # Número de páginas de Google a procesar por cada búsqueda
    "num_pages": 2,

    # Tiempo de espera entre páginas (segundos)
    "page_delay": 3,
}

# Configuración del navegador
BROWSER_CONFIG = {
    # Ejecutar en modo headless (sin interfaz gráfica)
    "headless": False,

    # User agent personalizado (opcional)
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    # Timeout implícito (segundos)
    "implicit_wait": 10,
}

# Configuración de salida
OUTPUT_CONFIG = {
    # Directorio donde se guardarán los resultados
    "output_dir": "data",

    # Nombre del archivo de salida (None para generar automáticamente con timestamp)
    "output_filename": None,

    # Formato de salida: 'csv' o 'json'
    "output_format": "csv",
}
