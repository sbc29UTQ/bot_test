# Paradigma Funcional en LinkedIn Profile Scraper

Este proyecto ha sido reestructurado siguiendo el **paradigma de programación funcional**. Este documento explica los conceptos aplicados y cómo usar el código.

## 📚 Conceptos de Programación Funcional Aplicados

### 1. **Funciones Puras**

Funciones que siempre retornan el mismo output para el mismo input, sin efectos secundarios.

```python
# Función pura - Transforma datos sin modificarlos
def build_search_query(keywords: List[str]) -> str:
    """
    Input: ["Director de Marketing", "Perú"]
    Output: 'site:linkedin.com/in "Director de Marketing" "Perú"'
    Siempre retorna lo mismo para el mismo input
    """
    quoted_keywords = map(lambda k: f'"{k}"', keywords)
    return "site:linkedin.com/in " + " ".join(quoted_keywords)

# Función pura - Limpia URL sin efectos secundarios
def clean_linkedin_url(url: str) -> Optional[str]:
    """Transforma una URL sucia en una limpia, sin modificar nada más"""
    # ... transformación pura
    return clean_url
```

### 2. **Inmutabilidad**

Los datos no se modifican, se crean nuevas versiones.

```python
# En lugar de modificar un objeto (OOP):
# self.profiles_data.append(profile)  # ❌ Muta el estado

# Creamos nuevo estado (Funcional):
new_state = {
    **state,  # Copia el estado actual
    'profiles_data': state['profiles_data'] + [profile]  # Nueva lista
}
```

### 3. **Composición de Funciones**

Combinar funciones pequeñas para crear funciones más complejas.

```python
# Funciones pequeñas y componibles
state = create_initial_state()
driver = create_driver(config)
query = build_search_query(keywords)
perform_search(driver, query, config['wait_time'], config['debug'])
new_state = extract_profiles_from_page(driver, state, config)

# O usando composición explícita
compose(
    save_results,
    filter_valid_profiles,
    extract_profiles,
    parse_html
)(page_source)
```

### 4. **Funciones de Orden Superior**

Funciones que reciben o retornan otras funciones.

```python
# Map - Transforma cada elemento
urls = list(map(lambda p: p['url'], profiles))

# Filter - Selecciona elementos que cumplen condición
valid_profiles = list(filter(lambda p: p['url'] is not None, profiles))

# Reduce - Acumula/agrega información
from functools import reduce
total = reduce(lambda acc, p: acc + len(p['profiles_data']), states, 0)
```

### 5. **Estado como Valor de Retorno**

En lugar de modificar un estado global, retornamos nuevo estado.

```python
# OOP (estado mutable):
class Scraper:
    def __init__(self):
        self.profiles = []  # Estado mutable

    def scrape(self):
        self.profiles.append(...)  # Modifica estado

# Funcional (estado inmutable):
def scrape(state: ScraperState, config: ScraperConfig) -> ScraperState:
    # No modifica state, retorna nuevo estado
    return {
        **state,
        'profiles_data': state['profiles_data'] + new_profiles
    }
```

## 🏗️ Arquitectura Funcional

### Tipos de Datos

```python
# Definimos tipos para claridad
ScraperConfig = Dict[str, any]   # Configuración inmutable
ProfileData = Dict[str, str]     # Datos de un perfil
ScraperState = Dict[str, any]    # Estado del scraper
```

### Estructura por Capas

```
1. CONFIGURACIÓN (Datos inmutables)
   ├── create_config()
   └── create_initial_state()

2. TRANSFORMACIONES PURAS (Input -> Output)
   ├── build_search_query()
   ├── clean_linkedin_url()
   ├── format_profile_entry()
   └── format_output()

3. OPERACIONES I/O (Efectos secundarios controlados)
   ├── create_driver()
   ├── perform_search()
   ├── navigate_to_next_page()
   └── save_results_to_file()

4. EXTRACCIÓN (Transformaciones con estado)
   ├── extract_profile_from_link()
   ├── extract_profile_from_result()
   └── extract_profiles_from_page()

5. COMPOSICIÓN (Orquestación)
   └── scrape_linkedin_profiles()  # Función principal
```

## 💻 Cómo Usar

### Uso Básico

```python
from src.linkedin_scraper import create_config, scrape_linkedin_profiles

# 1. Crear configuración inmutable
config = create_config(
    headless=False,
    debug=True,
    num_pages=2,
    wait_time=5
)

# 2. Definir keywords
keywords = ["Director de Marketing Digital", "Perú"]

# 3. Ejecutar (retorna estado con resultados)
state = scrape_linkedin_profiles(keywords, config, "output.txt")

# 4. Acceder a resultados
profiles = state['profiles_data']
print(f"Perfiles encontrados: {len(profiles)}")
```

### Uso Simplificado

```python
from src.linkedin_scraper import run_scraper

# Función auxiliar que encapsula la configuración
profiles = run_scraper(
    keywords=["Data Scientist", "Lima"],
    num_pages=2,
    output_file="results.txt",
    headless=False,
    debug=True
)
```

### Composición Funcional

```python
from functools import reduce

# Múltiples búsquedas usando reduce
searches = [
    (["CEO", "startup"], "ceo.txt"),
    (["CTO", "tech"], "cto.txt"),
]

def accumulate_results(acc, search_params):
    keywords, filename = search_params
    config = create_config(headless=True, num_pages=1)
    state = scrape_linkedin_profiles(keywords, config, filename)
    return acc + state['profiles_data']

all_profiles = reduce(accumulate_results, searches, [])
```

## 🔄 Comparación OOP vs Funcional

### Antes (OOP)

```python
class LinkedInProfileScraper:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.profiles_data = []  # Estado mutable

    def run(self, keywords, num_pages):
        self.setup_driver()  # Modifica self.driver
        self.search_google(keywords)  # Modifica estado interno
        self.save_results()  # Lee de self.profiles_data
        self.close()

# Uso
scraper = LinkedInProfileScraper(headless=False)
scraper.run(["Marketing", "Perú"], 2)
# Estado oculto en scraper.profiles_data
```

### Ahora (Funcional)

```python
# Funciones puras y composición
config = create_config(headless=False, num_pages=2)
keywords = ["Marketing", "Perú"]

# Estado explícito, retornado por la función
state = scrape_linkedin_profiles(keywords, config, "output.txt")

# Estado visible y accesible
profiles = state['profiles_data']
```

## ✅ Ventajas del Enfoque Funcional

### 1. **Predecibilidad**
- Funciones puras siempre retornan lo mismo
- No hay efectos secundarios ocultos
- Más fácil de razonar sobre el código

### 2. **Testabilidad**
```python
# Fácil de testear (no necesita mocks)
def test_build_query():
    result = build_search_query(["CEO", "Lima"])
    assert result == 'site:linkedin.com/in "CEO" "Lima"'

def test_clean_url():
    dirty = "https://linkedin.com/in/john-doe?param=123"
    clean = clean_linkedin_url(dirty)
    assert clean == "https://linkedin.com/in/john-doe"
```

### 3. **Composabilidad**
```python
# Funciones pequeñas se pueden combinar
pipeline = compose(
    save_to_file,
    format_results,
    filter_valid,
    extract_profiles
)

result = pipeline(html_source)
```

### 4. **Reusabilidad**
```python
# Funciones puras se pueden reusar fácilmente
clean_url_1 = clean_linkedin_url(url1)
clean_url_2 = clean_linkedin_url(url2)

# No hay estado compartido, no hay side effects
```

### 5. **Paralelización**
```python
# Funciones puras son fáciles de paralelizar
from multiprocessing import Pool

with Pool(4) as p:
    clean_urls = p.map(clean_linkedin_url, dirty_urls)
```

## 📖 Principios Aplicados

### 1. **Separación de Concerns**
- Transformaciones puras separadas de I/O
- Configuración separada de lógica
- Estado explícito, no oculto

### 2. **Single Responsibility**
- Cada función hace una cosa
- `clean_linkedin_url` solo limpia URLs
- `build_search_query` solo construye queries
- `extract_profile` solo extrae un perfil

### 3. **DRY con Funciones**
- Reusar funciones puras
- Componer en lugar de duplicar
- Map/Filter/Reduce en lugar de loops

## 🎯 Patrones Funcionales Usados

### Map - Transformar colección
```python
urls = list(map(lambda p: p['url'], profiles))
```

### Filter - Filtrar colección
```python
valid = list(filter(lambda p: p['url'], profiles))
```

### Reduce - Agregar colección
```python
total = reduce(lambda acc, p: acc + [p], profiles, [])
```

### Compose - Combinar funciones
```python
process = compose(step3, step2, step1)
result = process(input)
```

### Pipe - Flujo de datos
```python
result = (
    input_data
    |> step1
    |> step2
    |> step3
)  # Python no tiene pipe operator, pero el concepto se aplica
```

## 📚 Recursos

- [Functional Programming in Python](https://docs.python.org/3/howto/functional.html)
- [Map, Filter, Reduce](https://book.pythontips.com/en/latest/map_filter.html)
- [functools - Higher-order functions](https://docs.python.org/3/library/functools.html)

## 🚀 Ejemplos Incluidos

1. **`main.py`**: Ejemplos básicos y avanzados
2. **`ejemplos/ejemplo_basico.py`**: Uso básico funcional
3. **`ejemplos/ejemplo_funcional_puro.py`**: Conceptos avanzados:
   - Pipeline funcional completo
   - Map/Filter/Reduce
   - Composición de funciones
   - Múltiples búsquedas con reduce

## 💡 Tips

1. **Piensa en transformaciones, no en mutaciones**
   - ❌ `list.append(item)`
   - ✅ `new_list = old_list + [item]`

2. **Retorna nuevo estado en lugar de modificar**
   - ❌ `self.data = new_data`
   - ✅ `return {'data': new_data}`

3. **Usa funciones pequeñas y combínalas**
   - ✅ Una función hace una cosa
   - ✅ Componer funciones para operaciones complejas

4. **Separa funciones puras de I/O**
   - ✅ Funciones de transformación (puras)
   - ✅ Funciones de I/O (efectos secundarios controlados)

---

**¿Preguntas?** Revisa los ejemplos en `ejemplos/ejemplo_funcional_puro.py` para ver estos conceptos en acción.
