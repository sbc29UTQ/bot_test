"""
Ejemplo en Modo Headless

Ejecuta el navegador sin interfaz gráfica (más rápido)
Útil para ejecución en servidores o cuando no necesitas ver el navegador
"""

from src.linkedin_scraper import LinkedInProfileScraper


def main():
    # Crear instancia en modo headless
    # headless=True ejecuta el navegador sin interfaz gráfica
    scraper = LinkedInProfileScraper(headless=True)

    keywords = [
        "CEO",
        "startup",
        "Lima"
    ]

    print("Ejecutando en modo HEADLESS (sin interfaz gráfica)")
    print(f"Keywords: {keywords}\n")

    scraper.run(
        keywords=keywords,
        num_pages=1,
        output_file="ceo_startup_lima.txt"
    )

    print("\n✅ Revisa el archivo: output/ceo_startup_lima.txt")


if __name__ == "__main__":
    main()
