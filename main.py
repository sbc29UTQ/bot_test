"""
Script principal para ejecutar el scraper de perfiles de LinkedIn
Paradigma Funcional - Composición de funciones
"""

from src.linkedin_scraper import (
    create_config,
    scrape_linkedin_profiles,
    run_scraper
)


def ejemplo_basico():
    """Ejemplo básico: Buscar Director de Marketing Digital en Perú"""
    print("\n" + "="*80)
    print("EJEMPLO 1: Director de Marketing Digital en Perú")
    print("="*80)

    # Crear configuración
    config = create_config(
        headless=False,
        debug=True,
        num_pages=2,
        wait_time=5
    )

    # Definir keywords
    keywords = [
        "Director de Marketing Digital",
        "Perú"
    ]

    # Ejecutar scraper (retorna estado con resultados)
    state = scrape_linkedin_profiles(
        keywords=keywords,
        config=config,
        output_file="marketing_digital_peru.txt"
    )

    print(f"\n✅ Perfiles encontrados: {len(state['profiles_data'])}")


def ejemplo_con_sector():
    """Ejemplo con sector específico: Marketing Digital en Retail en Perú"""
    print("\n" + "="*80)
    print("EJEMPLO 2: Director de Marketing Digital en Retail, Perú")
    print("="*80)

    config = create_config(headless=False, debug=False, num_pages=2)

    keywords = [
        "Director de Marketing Digital",
        "retail",
        "Perú"
    ]

    state = scrape_linkedin_profiles(keywords, config, "marketing_retail_peru.txt")
    print(f"\n✅ Perfiles encontrados: {len(state['profiles_data'])}")


def ejemplo_simplificado():
    """Ejemplo usando la función auxiliar simplificada"""
    print("\n" + "="*80)
    print("EJEMPLO 3: Uso simplificado de run_scraper()")
    print("="*80)

    # Función auxiliar que encapsula la creación de config
    profiles = run_scraper(
        keywords=["Data Scientist", "Lima"],
        num_pages=1,
        output_file="data_science_lima.txt",
        headless=False,
        debug=True
    )

    print(f"\n✅ Perfiles encontrados: {len(profiles)}")


def ejemplo_funcional_avanzado():
    """Ejemplo mostrando composición funcional"""
    print("\n" + "="*80)
    print("EJEMPLO 4: Composición Funcional")
    print("="*80)

    # Composición: crear config -> ejecutar scraper -> procesar resultados
    from functools import reduce

    # Lista de búsquedas a realizar
    searches = [
        (["CEO", "startup"], "ceo_startup.txt"),
        (["CTO", "tech"], "cto_tech.txt"),
    ]

    # Función para acumular resultados
    def accumulate_results(acc, search_params):
        keywords, filename = search_params
        config = create_config(headless=True, debug=False, num_pages=1)
        state = scrape_linkedin_profiles(keywords, config, filename)
        return acc + state['profiles_data']

    # Reducir todas las búsquedas a una lista de perfiles
    all_profiles = reduce(accumulate_results, searches, [])

    print(f"\n✅ Total de perfiles en todas las búsquedas: {len(all_profiles)}")


def main():
    """
    Función principal
    Descomenta el ejemplo que quieras ejecutar
    """

    # Ejecutar ejemplo básico
    ejemplo_basico()

    # Ejecutar ejemplo con sector
    # ejemplo_con_sector()

    # Ejecutar ejemplo simplificado
    # ejemplo_simplificado()

    # Ejecutar ejemplo funcional avanzado
    # ejemplo_funcional_avanzado()


if __name__ == "__main__":
    main()
