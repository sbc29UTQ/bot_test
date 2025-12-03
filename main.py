"""
Script principal para ejecutar el scraper de perfiles de LinkedIn
"""

from src.linkedin_scraper import LinkedInProfileScraper


def ejemplo_basico():
    """Ejemplo básico: Buscar Director de Marketing Digital en Perú"""
    print("\n" + "="*80)
    print("EJEMPLO 1: Director de Marketing Digital en Perú")
    print("="*80)

    scraper = LinkedInProfileScraper(headless=False)

    keywords = [
        "Director de Marketing Digital",
        "Perú"
    ]

    scraper.run(
        keywords=keywords,
        num_pages=2,
        output_file="marketing_digital_peru.txt"
    )


def ejemplo_con_sector():
    """Ejemplo con sector específico: Marketing Digital en Retail en Perú"""
    print("\n" + "="*80)
    print("EJEMPLO 2: Director de Marketing Digital en Retail, Perú")
    print("="*80)

    scraper = LinkedInProfileScraper(headless=False)

    keywords = [
        "Director de Marketing Digital",
        "retail",
        "Perú"
    ]

    scraper.run(
        keywords=keywords,
        num_pages=2,
        output_file="marketing_retail_peru.txt"
    )


def ejemplo_personalizado():
    """Personaliza este ejemplo con tus propias keywords"""
    print("\n" + "="*80)
    print("EJEMPLO PERSONALIZADO")
    print("="*80)

    scraper = LinkedInProfileScraper(headless=False)

    # Personaliza estas keywords según tus necesidades
    keywords = [
        "Data Scientist",       # Puesto o rol
        "Python",              # Skill o tecnología
        "Lima"                 # Ubicación
    ]

    scraper.run(
        keywords=keywords,
        num_pages=1,           # Ajusta el número de páginas
        output_file="busqueda_personalizada.txt"
    )


def main():
    """
    Función principal
    Descomenta el ejemplo que quieras ejecutar
    """

    # Ejecutar ejemplo básico
    ejemplo_basico()

    # Ejecutar ejemplo con sector
    # ejemplo_con_sector()

    # Ejecutar ejemplo personalizado
    # ejemplo_personalizado()


if __name__ == "__main__":
    main()
