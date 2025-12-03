"""
Ejemplo Básico - Paradigma Funcional
Buscar Director de Marketing Digital en Perú

Búsqueda en Google: site:linkedin.com/in "Director de Marketing Digital" "Perú"
"""

from src.linkedin_scraper import create_config, scrape_linkedin_profiles


def main():
    # Crear configuración inmutable
    config = create_config(
        headless=False,  # Ver el navegador
        debug=True,      # Modo debug activado
        num_pages=2,     # Procesar 2 páginas
        wait_time=5      # Esperar 5 segundos
    )

    # Definir keywords (lista inmutable)
    keywords = [
        "Director de Marketing Digital",
        "Perú"
    ]

    print("Iniciando búsqueda:")
    print(f"Keywords: {keywords}")
    print(f"Búsqueda en Google: site:linkedin.com/in \"Director de Marketing Digital\" \"Perú\"\n")

    # Ejecutar scraper (función pura que retorna estado)
    state = scrape_linkedin_profiles(
        keywords=keywords,
        config=config,
        output_file="marketing_digital_peru.txt"
    )

    # Acceder a los resultados del estado retornado
    profiles_found = state['profiles_data']

    print(f"\n✅ Revisa el archivo: output/marketing_digital_peru.txt")
    print(f"   Total de perfiles: {len(profiles_found)}")


if __name__ == "__main__":
    main()
