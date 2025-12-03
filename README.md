# LinkedIn Profile Scraper

Herramienta en Python para buscar y recopilar URLs de perfiles de LinkedIn utilizando búsquedas en Google con Selenium y BeautifulSoup.

## 📋 Características

- 🔍 Búsqueda automatizada de perfiles de LinkedIn usando Google
- 🤖 Automatización con Selenium WebDriver
- 🧹 Parsing y limpieza de URLs con BeautifulSoup
- 💾 Exportación de resultados a CSV
- ⚙️ Configuración personalizable
- 🎯 Búsqueda por keywords específicas
- 📄 Soporte para múltiples páginas de resultados

## 🛠️ Requisitos

- Python 3.8 o superior
- Google Chrome instalado
- ChromeDriver (se instala automáticamente con webdriver-manager)

## 📦 Instalación

1. Clona el repositorio:
```bash
git clone <repository-url>
cd bot_test
```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv venv

# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Uso básico

Ejecuta el script principal:

```bash
python main.py
```

### Personalización

#### Opción 1: Editar main.py

Abre `main.py` y modifica los parámetros:

```python
# Cambiar las keywords de búsqueda
keywords = [
    "python developer",
    "data scientist",
    "machine learning"
]

# O usar un string
keywords = "senior software engineer remote"

# Ejecutar el scraper
scraper.run(
    keywords=keywords,
    num_pages=3,  # Número de páginas de Google a procesar
    output_file="mi_archivo.csv"  # Nombre del archivo de salida
)
```

#### Opción 2: Usar el scraper en tu propio código

```python
from src.linkedin_scraper import LinkedInProfileScraper

# Crear instancia
scraper = LinkedInProfileScraper(headless=False)

# Ejecutar búsqueda
scraper.run(
    keywords="python developer remote",
    num_pages=2,
    output_file="profiles.csv"
)
```

### Modo headless

Para ejecutar el navegador sin interfaz gráfica:

```python
scraper = LinkedInProfileScraper(headless=True)
```

## 📁 Estructura del Proyecto

```
bot_test/
├── src/
│   ├── __init__.py
│   └── linkedin_scraper.py    # Clase principal del scraper
├── data/                       # Carpeta donde se guardan los resultados
├── logs/                       # Carpeta para logs (futuro)
├── main.py                     # Script principal de ejecución
├── config.example.py           # Archivo de configuración de ejemplo
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

## 📊 Formato de Salida

Los resultados se guardan en formato CSV en la carpeta `data/`:

```csv
Profile URL
https://linkedin.com/in/johndoe
https://linkedin.com/in/janedoe
https://linkedin.com/in/alexsmith
```

El nombre del archivo incluye un timestamp automático:
```
linkedin_profiles_20231203_143025.csv
```

## ⚙️ Configuración

### Parámetros del Scraper

- `headless` (bool): Ejecutar navegador sin interfaz gráfica
- `keywords` (str o list): Keywords para buscar
- `num_pages` (int): Número de páginas de resultados de Google
- `output_file` (str): Nombre del archivo de salida

### Ejemplo de búsqueda avanzada

```python
scraper = LinkedInProfileScraper(headless=False)

# Búsqueda específica por rol y ubicación
scraper.run(
    keywords="senior data scientist Madrid",
    num_pages=5,
    output_file="data_scientists_madrid.csv"
)
```

## 🔍 Cómo Funciona

1. El scraper abre Google Chrome usando Selenium
2. Realiza una búsqueda con el formato: `site:linkedin.com/in/ {keywords}`
3. Parsea los resultados con BeautifulSoup
4. Extrae y limpia las URLs de perfiles de LinkedIn
5. Navega por múltiples páginas de resultados
6. Guarda todos los perfiles únicos en un archivo CSV

## ⚠️ Consideraciones Importantes

1. **Rate Limiting**: Google puede bloquear búsquedas automatizadas si se hacen muchas peticiones rápidamente. Usa el scraper de forma responsable.

2. **Términos de Servicio**: Asegúrate de cumplir con los términos de servicio de Google y LinkedIn.

3. **Captchas**: Google puede mostrar captchas si detecta comportamiento automatizado.

4. **Permisos**: Este proyecto es solo para fines educativos y de investigación.

## 🐛 Solución de Problemas

### Error: ChromeDriver not found

El script usa `webdriver-manager` que descarga ChromeDriver automáticamente. Si hay problemas:

```bash
pip install --upgrade webdriver-manager
```

### Error: Chrome binary not found

Asegúrate de tener Google Chrome instalado en tu sistema.

### No se encuentran resultados

- Verifica tu conexión a internet
- Prueba con keywords diferentes
- Reduce el número de páginas a procesar
- Intenta ejecutar en modo no headless para ver qué sucede

## 📝 Ejemplos de Uso

### Ejemplo 1: Buscar desarrolladores Python

```python
from src.linkedin_scraper import LinkedInProfileScraper

scraper = LinkedInProfileScraper(headless=False)
scraper.run(
    keywords="python developer",
    num_pages=3,
    output_file="python_devs.csv"
)
```

### Ejemplo 2: Buscar múltiples perfiles

```python
from src.linkedin_scraper import LinkedInProfileScraper

keywords_list = [
    "data scientist",
    "machine learning engineer",
    "AI researcher"
]

scraper = LinkedInProfileScraper(headless=True)

for keyword in keywords_list:
    print(f"\nBuscando: {keyword}")
    scraper.setup_driver()
    scraper.search_google(keyword, num_pages=2)
    scraper.close()

scraper.save_results("all_profiles.csv")
```

## 🔄 Próximas Mejoras

- [ ] Soporte para exportación a JSON
- [ ] Sistema de logging mejorado
- [ ] Configuración desde archivo .env
- [ ] Manejo de captchas
- [ ] Proxy support
- [ ] Filtros adicionales de búsqueda

## 📄 Licencia

Este proyecto es solo para fines educativos y de investigación.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor abre un issue o pull request.

## ⚡ Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el scraper
python main.py

# Los resultados estarán en: data/linkedin_profiles_[timestamp].csv
```

---

**Nota**: Usa esta herramienta de forma responsable y ética. Respeta la privacidad de los usuarios y cumple con todos los términos de servicio aplicables.
