"""
Ejemplo Básico: Buscar Director de Marketing Digital en Perú

Búsqueda en Google: site:linkedin.com/in "Director de Marketing Digital" "Perú"
"""

from src.linkedin_scraper import LinkedInProfileScraper


def main():
    # Crear instancia del scraper
    # headless=False para ver el navegador en acción
    scraper = LinkedInProfileScraper(headless=False)

    # Definir las keywords de búsqueda
    keywords = [
        "Director de Marketing Digital",
        "Perú"
    ]

    print("Iniciando búsqueda:")
    print(f"Keywords: {keywords}")
    print(f"Búsqueda en Google: site:linkedin.com/in \"Director de Marketing Digital\" \"Perú\"\n")

    # Ejecutar el scraper
    scraper.run(
        keywords=keywords,
        num_pages=2,  # Procesar 2 páginas de resultados de Google
        output_file="marketing_digital_peru.txt"
    )

    print("\n✅ Revisa el archivo: output/marketing_digital_peru.txt")


if __name__ == "__main__":
    main()
