# LinkedIn Profile Scraper

Herramienta en Python para buscar y extraer URLs de perfiles de LinkedIn utilizando búsquedas avanzadas en Google con Selenium y BeautifulSoup.

## 📋 Descripción

Este scraper automatiza la búsqueda de perfiles de LinkedIn en Google utilizando el formato:
```
site:linkedin.com/in "keyword1" "keyword2" "keyword3"
```

Por ejemplo:
- `site:linkedin.com/in "Director de Marketing Digital" "Perú"`
- `site:linkedin.com/in "Director de Marketing Digital" "retail" "Perú"`

Los resultados se guardan en archivos TXT con información detallada de cada perfil.

## 🎯 Características

- 🔍 **Búsquedas precisas** con múltiples keywords entre comillas
- 🤖 **Automatización completa** con Selenium WebDriver
- 🧹 **Extracción y limpieza** de URLs con BeautifulSoup
- 📝 **Exportación a TXT** con información detallada
- ⚙️ **Modo headless** opcional (sin interfaz gráfica)
- 📄 **Múltiples páginas** de resultados de Google
- 📊 **Información adicional** (título, descripción) de cada perfil

## 🛠️ Requisitos

- Python 3.8 o superior
- Google Chrome instalado
- ChromeDriver (se instala automáticamente con webdriver-manager)

## 📦 Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd bot_test
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv venv

# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## 📁 Estructura del Proyecto

```
proyecto/
├── README.md                      # Este archivo
├── TROUBLESHOOTING.md            # Solución de problemas
├── requirements.txt               # Dependencias del proyecto
├── main.py                        # Script principal de ejecución
├── config.example.py              # Configuración de ejemplo
├── src/
│   ├── __init__.py
│   └── linkedin_scraper.py       # Clase principal del scraper
├── ejemplos/
│   ├── README.md                 # Documentación de ejemplos
│   ├── ejemplo_basico.py         # Ejemplo básico
│   ├── ejemplo_con_sector.py     # Ejemplo con sector específico
│   ├── ejemplo_headless.py       # Ejemplo en modo headless
│   └── ejemplo_multiple_busquedas.py  # Múltiples búsquedas
└── output/                        # Carpeta donde se guardan los resultados TXT
```

## 🚀 Uso Rápido

### Opción 1: Ejecutar el script principal

```bash
python main.py
```

### Opción 2: Ejecutar un ejemplo

```bash
# Ejemplo básico
python ejemplos/ejemplo_basico.py

# Ejemplo con sector
python ejemplos/ejemplo_con_sector.py

# Ejemplo en modo headless (sin interfaz gráfica)
python ejemplos/ejemplo_headless.py

# Múltiples búsquedas
python ejemplos/ejemplo_multiple_busquedas.py
```

## 💡 Ejemplos de Uso

### Ejemplo 1: Búsqueda Básica

```python
from src.linkedin_scraper import LinkedInProfileScraper

# Crear instancia del scraper
scraper = LinkedInProfileScraper(headless=False)

# Definir keywords
keywords = [
    "Director de Marketing Digital",
    "Perú"
]

# Ejecutar búsqueda
# Google buscará: site:linkedin.com/in "Director de Marketing Digital" "Perú"
scraper.run(
    keywords=keywords,
    num_pages=2,
    output_file="marketing_peru.txt"
)
```

**Resultado:** Se guardará en `output/marketing_peru.txt`

### Ejemplo 2: Búsqueda con Sector

```python
from src.linkedin_scraper import LinkedInProfileScraper

scraper = LinkedInProfileScraper(headless=False)

keywords = [
    "Director de Marketing Digital",
    "retail",
    "Perú"
]

# Google buscará: site:linkedin.com/in "Director de Marketing Digital" "retail" "Perú"
scraper.run(
    keywords=keywords,
    num_pages=2,
    output_file="marketing_retail_peru.txt"
)
```

### Ejemplo 3: Modo Headless (sin interfaz gráfica)

```python
from src.linkedin_scraper import LinkedInProfileScraper

# headless=True para ejecutar sin ver el navegador
scraper = LinkedInProfileScraper(headless=True)

keywords = ["Data Scientist", "Lima"]

scraper.run(
    keywords=keywords,
    num_pages=1,
    output_file="data_science_lima.txt"
)
```

## 📊 Formato de Salida (TXT)

Los resultados se guardan en formato TXT en la carpeta `output/`:

```
================================================================================
PERFILES DE LINKEDIN ENCONTRADOS
================================================================================

Búsqueda realizada: site:linkedin.com/in "Director de Marketing Digital" "Perú"
Fecha: 2024-12-03 14:30:25
Total de perfiles encontrados: 15

================================================================================

PERFIL #1
--------------------------------------------------------------------------------
URL: https://www.linkedin.com/in/carla-medina-lazo
Título: Carla Medina Lazo - Director de Marketing Digital - Company
Descripción: Experiencia en marketing digital y estrategias...

PERFIL #2
--------------------------------------------------------------------------------
URL: https://www.linkedin.com/in/juan-perez
Título: Juan Pérez - Marketing Manager
Descripción: ...

...

================================================================================
RESUMEN - SOLO URLs
================================================================================

https://www.linkedin.com/in/carla-medina-lazo
https://www.linkedin.com/in/juan-perez
...
```

## ⚙️ Configuración

### Parámetros del Scraper

| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `headless` | bool | Ejecutar navegador sin interfaz gráfica | False |
| `keywords` | list | Lista de keywords para búsqueda | - |
| `num_pages` | int | Número de páginas de resultados de Google | 1 |
| `output_file` | str | Nombre del archivo de salida | auto |

### Personalización

Edita `main.py` para personalizar tu búsqueda:

```python
# Cambiar las keywords
keywords = [
    "CEO",              # Puesto
    "startup",          # Sector/industria
    "Lima"             # Ubicación
]

# Ajustar número de páginas
num_pages = 3  # Más páginas = más resultados

# Modo headless
scraper = LinkedInProfileScraper(headless=True)
```

## 🔍 Cómo Funciona

1. **Construcción de búsqueda:** Cada keyword se pone entre comillas
   - Input: `["Director de Marketing", "Perú"]`
   - Output: `site:linkedin.com/in "Director de Marketing" "Perú"`

2. **Automatización:** Selenium abre Google Chrome y realiza la búsqueda

3. **Extracción:** BeautifulSoup parsea los resultados y extrae:
   - URL del perfil de LinkedIn
   - Título del resultado
   - Descripción/snippet

4. **Limpieza:** Las URLs se limpian y normalizan

5. **Guardado:** Los resultados se guardan en formato TXT en `output/`

## 🎓 Tips de Uso

### Keywords Efectivas

✅ **Buenas combinaciones:**
```python
# Puesto + Ubicación
keywords = ["CEO", "Lima"]

# Puesto + Industria + Ubicación
keywords = ["Director de Marketing", "retail", "Perú"]

# Skill + Ubicación
keywords = ["Python Developer", "remote"]

# Puesto + Empresa
keywords = ["Data Scientist", "Google"]
```

❌ **Evitar:**
- Demasiadas keywords (>5) → Muy pocos resultados
- Keywords muy genéricas sin filtros → Resultados irrelevantes

### Número de Páginas

- `num_pages=1`: ~10 perfiles
- `num_pages=2`: ~20 perfiles
- `num_pages=3`: ~30 perfiles
- `num_pages=5`: ~50 perfiles

⚠️ **Nota:** Google puede mostrar CAPTCHAs si procesas muchas páginas rápidamente.

### Optimizar Velocidad

```python
# Usar modo headless (más rápido)
scraper = LinkedInProfileScraper(headless=True)

# Procesar menos páginas
scraper.run(keywords=keywords, num_pages=1)
```

### Múltiples Búsquedas

Si necesitas hacer varias búsquedas, agrega delays entre ellas:

```python
import time

busquedas = [
    ["Marketing", "Lima"],
    ["Engineering", "Lima"],
    ["Sales", "Lima"]
]

for keywords in busquedas:
    scraper = LinkedInProfileScraper(headless=True)
    scraper.run(keywords=keywords, num_pages=1)
    time.sleep(60)  # Esperar 60 segundos entre búsquedas
```

## ⚠️ Consideraciones Importantes

1. **Rate Limiting:** Google puede bloquear búsquedas automatizadas. Usa el scraper de forma responsable.

2. **CAPTCHAs:** Google puede mostrar CAPTCHAs si detecta comportamiento automatizado.

3. **Términos de Servicio:** Cumple con los términos de servicio de Google y LinkedIn.

4. **Uso Educativo:** Este proyecto es solo para fines educativos y de investigación.

## 🐛 Solución de Problemas

### Error al instalar lxml

**Solución:** El proyecto ya usa `html.parser` (incluido con Python). Simplemente instala:
```bash
pip install -r requirements.txt
```

Ver más soluciones en [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### No se encuentran perfiles

1. Verifica tu conexión a internet
2. Prueba con keywords diferentes
3. Ejecuta en modo no-headless para ver qué sucede
4. Google puede estar mostrando un CAPTCHA

### ChromeDriver error

```bash
pip install --upgrade webdriver-manager
```

## 📚 Documentación Adicional

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solución de problemas comunes
- [ejemplos/README.md](ejemplos/README.md) - Documentación de ejemplos
- [config.example.py](config.example.py) - Configuración de ejemplo

## 🔄 Próximas Mejoras

- [ ] Exportación a CSV y JSON
- [ ] Interfaz de línea de comandos (CLI)
- [ ] Configuración desde archivo .env
- [ ] Sistema de logging mejorado
- [ ] Manejo automático de CAPTCHAs
- [ ] Soporte para proxies

## ⚡ Inicio Rápido (TL;DR)

```bash
# 1. Instalar
pip install -r requirements.txt

# 2. Ejecutar
python main.py

# 3. Ver resultados
cat output/*.txt
```

## 📄 Licencia

Este proyecto es solo para fines educativos y de investigación.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor abre un issue o pull request.

---

**⚠️ Disclaimer:** Usa esta herramienta de forma responsable y ética. Respeta la privacidad de los usuarios y cumple con todos los términos de servicio aplicables.
