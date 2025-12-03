"""
Ejemplo con Sector: Buscar Director de Marketing Digital en Retail, Perú

Búsqueda en Google: site:linkedin.com/in "Director de Marketing Digital" "retail" "Perú"
"""

from src.linkedin_scraper import LinkedInProfileScraper


def main():
    # Crear instancia del scraper
    scraper = LinkedInProfileScraper(headless=False)

    # Definir las keywords de búsqueda
    # Puedes agregar más keywords para refinar la búsqueda
    keywords = [
        "Director de Marketing Digital",
        "retail",
        "Perú"
    ]

    print("Iniciando búsqueda:")
    print(f"Keywords: {keywords}")
    print(f"Búsqueda en Google: site:linkedin.com/in \"Director de Marketing Digital\" \"retail\" \"Perú\"\n")

    # Ejecutar el scraper
    scraper.run(
        keywords=keywords,
        num_pages=2,
        output_file="marketing_retail_peru.txt"
    )

    print("\n✅ Revisa el archivo: output/marketing_retail_peru.txt")


if __name__ == "__main__":
    main()
