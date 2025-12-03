"""
Ejemplo de Programación Funcional Pura
Demuestra los principios de programación funcional:
- Funciones puras
- Inmutabilidad
- Composición de funciones
- Map, Filter, Reduce
"""

from src.linkedin_scraper import (
    create_config,
    build_search_query,
    scrape_linkedin_profiles,
    clean_linkedin_url
)
from functools import reduce
from typing import List, Dict


# =============================================================================
# FUNCIONES PURAS - No modifican datos, solo transforman
# =============================================================================

def create_search_params(role: str, location: str) -> List[str]:
    """
    Función pura: crea parámetros de búsqueda.
    Input -> Output, sin efectos secundarios.
    """
    return [role, location]


def extract_urls_from_profiles(profiles: List[Dict]) -> List[str]:
    """
    Función pura: extrae solo las URLs de los perfiles.
    Usa map para transformar datos.
    """
    return list(map(lambda p: p['url'], profiles))


def filter_profiles_with_title(profiles: List[Dict]) -> List[Dict]:
    """
    Función pura: filtra perfiles que tienen título.
    Usa filter para seleccionar elementos.
    """
    return list(filter(lambda p: p['title'] != "Sin título", profiles))


def count_profiles_by_length(profiles: List[Dict]) -> Dict[str, int]:
    """
    Función pura: cuenta perfiles por longitud de título.
    Usa reduce para agregar información.
    """
    def categorize(acc, profile):
        title_length = len(profile['title'])
        if title_length < 30:
            category = 'corto'
        elif title_length < 60:
            category = 'medio'
        else:
            category = 'largo'

        acc[category] = acc.get(category, 0) + 1
        return acc

    return reduce(categorize, profiles, {})


# =============================================================================
# COMPOSICIÓN DE FUNCIONES
# =============================================================================

def compose(*functions):
    """
    Compone múltiples funciones en una sola.
    compose(f, g, h)(x) == f(g(h(x)))
    """
    def inner(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result
    return inner


# =============================================================================
# PIPELINE FUNCIONAL
# =============================================================================

def functional_pipeline_example():
    """
    Ejemplo de pipeline funcional completo:
    1. Crear config (inmutable)
    2. Ejecutar búsqueda
    3. Transformar resultados
    4. Filtrar datos
    5. Agregar información
    """
    print("=" * 80)
    print("EJEMPLO: Pipeline Funcional Puro")
    print("=" * 80)

    # Paso 1: Crear configuración inmutable
    config = create_config(headless=True, debug=False, num_pages=1)

    # Paso 2: Crear keywords usando función pura
    keywords = create_search_params("Data Scientist", "remote")

    print(f"\n📝 Query generada: {build_search_query(keywords)}")

    # Paso 3: Ejecutar scraper (función que retorna nuevo estado)
    state = scrape_linkedin_profiles(keywords, config, "functional_example.txt")

    profiles = state['profiles_data']

    if not profiles:
        print("\n⚠️ No se encontraron perfiles")
        return

    # Paso 4: Pipeline de transformaciones funcionales
    print(f"\n🔄 Aplicando transformaciones funcionales...")

    # Map: Extraer URLs
    urls = extract_urls_from_profiles(profiles)
    print(f"  • URLs extraídas: {len(urls)}")

    # Filter: Filtrar perfiles con título
    profiles_with_title = filter_profiles_with_title(profiles)
    print(f"  • Perfiles con título: {len(profiles_with_title)}")

    # Reduce: Contar por categoría
    categories = count_profiles_by_length(profiles_with_title)
    print(f"  • Categorías: {categories}")

    # Paso 5: Composición de funciones
    # Crear una función compuesta que hace todo el pipeline
    process_profiles = compose(
        count_profiles_by_length,
        filter_profiles_with_title
    )

    result = process_profiles(profiles)
    print(f"\n📊 Resultado final del pipeline: {result}")


def multiple_searches_functional():
    """
    Ejemplo de múltiples búsquedas usando reduce
    """
    print("\n" + "=" * 80)
    print("EJEMPLO: Múltiples Búsquedas con Reduce")
    print("=" * 80)

    # Lista de búsquedas (inmutable)
    searches = [
        (["Python Developer", "remote"], "python_remote.txt"),
        (["JavaScript Developer", "remote"], "js_remote.txt"),
        (["DevOps Engineer", "remote"], "devops_remote.txt"),
    ]

    # Función acumuladora
    def accumulate_profiles(accumulated_state, search_params):
        keywords, filename = search_params
        config = create_config(headless=True, debug=False, num_pages=1)

        print(f"\n🔍 Buscando: {' '.join(keywords)}")

        state = scrape_linkedin_profiles(keywords, config, filename)

        # Retornar nuevo estado acumulado (inmutabilidad)
        return {
            'total_profiles': accumulated_state['total_profiles'] + state['profiles_data'],
            'searches_completed': accumulated_state['searches_completed'] + 1
        }

    # Estado inicial
    initial_state = {'total_profiles': [], 'searches_completed': 0}

    # Reducir todas las búsquedas
    final_state = reduce(accumulate_profiles, searches, initial_state)

    print(f"\n" + "=" * 80)
    print(f"✅ Búsquedas completadas: {final_state['searches_completed']}")
    print(f"✅ Total de perfiles: {len(final_state['total_profiles'])}")
    print("=" * 80)


def main():
    """
    Función principal que ejecuta los ejemplos funcionales
    """

    # Ejemplo 1: Pipeline funcional completo
    functional_pipeline_example()

    # Ejemplo 2: Múltiples búsquedas con reduce
    # Descomenta para ejecutar:
    # multiple_searches_functional()


if __name__ == "__main__":
    main()
