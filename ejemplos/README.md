# Ejemplos de Uso

Esta carpeta contiene ejemplos prácticos de cómo usar el LinkedIn Profile Scraper.

## Archivos de Ejemplo

### 1. `ejemplo_basico.py`
Búsqueda simple con dos keywords:
- **Búsqueda:** `site:linkedin.com/in "Director de Marketing Digital" "Perú"`
- **Uso:** Ideal para empezar

```bash
python ejemplos/ejemplo_basico.py
```

### 2. `ejemplo_con_sector.py`
Búsqueda con sector específico:
- **Búsqueda:** `site:linkedin.com/in "Director de Marketing Digital" "retail" "Perú"`
- **Uso:** Cuando quieres agregar filtros adicionales como industria

```bash
python ejemplos/ejemplo_con_sector.py
```

### 3. `ejemplo_headless.py`
Ejecuta el navegador sin interfaz gráfica:
- **Modo:** Headless (sin ventana de navegador)
- **Uso:** Para ejecución más rápida o en servidores

```bash
python ejemplos/ejemplo_headless.py
```

### 4. `ejemplo_multiple_busquedas.py`
Ejecuta varias búsquedas en una sola ejecución:
- **Búsquedas:** Múltiples
- **Uso:** Para procesar varias búsquedas automáticamente

```bash
python ejemplos/ejemplo_multiple_busquedas.py
```

## Cómo Personalizar

Todos los ejemplos siguen la misma estructura:

```python
from src.linkedin_scraper import LinkedInProfileScraper

# 1. Crear instancia del scraper
scraper = LinkedInProfileScraper(headless=False)

# 2. Definir keywords (cada una irá entre comillas en Google)
keywords = [
    "Director de Marketing Digital",  # Puesto
    "retail",                         # Industria/sector
    "Perú"                           # Ubicación
]

# 3. Ejecutar búsqueda
scraper.run(
    keywords=keywords,
    num_pages=2,                      # Páginas de resultados
    output_file="mi_busqueda.txt"    # Archivo de salida
)
```

## Tips

### Keywords Efectivas

✅ **Buenas combinaciones:**
- Puesto + Ubicación: `["CEO", "Lima"]`
- Puesto + Industria + Ubicación: `["Director de Marketing", "retail", "Perú"]`
- Skill + Ubicación: `["Python Developer", "remote"]`

❌ **Evitar:**
- Demasiadas keywords (más de 4-5) puede limitar mucho los resultados
- Keywords muy genéricas sin filtros

### Número de Páginas

- `num_pages=1`: ~10 perfiles
- `num_pages=2`: ~20 perfiles
- `num_pages=3`: ~30 perfiles

**Nota:** Google puede mostrar CAPTCHAs si procesas muchas páginas rápidamente.

### Modo Headless

```python
# Ver el navegador (útil para debugging)
scraper = LinkedInProfileScraper(headless=False)

# Sin interfaz gráfica (más rápido)
scraper = LinkedInProfileScraper(headless=True)
```

## Resultados

Todos los resultados se guardan en la carpeta `output/` en formato TXT con:
- URL del perfil
- Título/nombre
- Descripción/snippet
- Resumen de URLs al final
