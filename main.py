"""
Script principal para ejecutar el scraper de perfiles de LinkedIn
"""

from src.linkedin_scraper import LinkedInProfileScraper


def main():
    """
    Función principal para ejecutar el scraper
    Personaliza los parámetros según tus necesidades
    """
    # Crear instancia del scraper
    # headless=True para ejecutar sin interfaz gráfica
    # headless=False para ver el navegador en acción
    scraper = LinkedInProfileScraper(headless=False)

    # Definir las keywords de búsqueda
    # Puedes usar una lista o un string
    keywords = [
        "python developer",
        "software engineer",
        "remote"
    ]

    # También puedes usar un string directamente
    # keywords = "python developer remote"

    print("Iniciando búsqueda de perfiles de LinkedIn...")
    print(f"Keywords: {' '.join(keywords) if isinstance(keywords, list) else keywords}")

    # Ejecutar el scraper
    scraper.run(
        keywords=keywords,
        num_pages=2,  # Número de páginas de resultados de Google
        output_file="linkedin_profiles.csv"  # Nombre del archivo de salida
    )

    print("\n✅ Proceso completado!")


if __name__ == "__main__":
    main()
