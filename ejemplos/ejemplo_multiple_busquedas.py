"""
Ejemplo de Múltiples Búsquedas

Ejecuta varias búsquedas diferentes en una sola ejecución
y guarda cada resultado en un archivo separado
"""

import time
from src.linkedin_scraper import LinkedInProfileScraper


def main():
    # Lista de búsquedas a realizar
    busquedas = [
        {
            "nombre": "Marketing Digital Perú",
            "keywords": ["Director de Marketing Digital", "Perú"],
            "archivo": "marketing_peru.txt"
        },
        {
            "nombre": "Data Science Lima",
            "keywords": ["Data Scientist", "Lima"],
            "archivo": "data_science_lima.txt"
        },
        {
            "nombre": "Software Engineer Python",
            "keywords": ["Software Engineer", "Python", "remote"],
            "archivo": "software_engineer_python.txt"
        }
    ]

    for i, busqueda in enumerate(busquedas, 1):
        print(f"\n{'='*80}")
        print(f"BÚSQUEDA {i}/{len(busquedas)}: {busqueda['nombre']}")
        print(f"{'='*80}")

        scraper = LinkedInProfileScraper(headless=True)  # headless para más rapidez

        scraper.run(
            keywords=busqueda['keywords'],
            num_pages=1,  # Solo 1 página por búsqueda
            output_file=busqueda['archivo']
        )

        # Esperar un poco entre búsquedas para evitar detección
        if i < len(busquedas):
            print("\nEsperando 30 segundos antes de la siguiente búsqueda...")
            time.sleep(30)

    print("\n" + "="*80)
    print("✅ TODAS LAS BÚSQUEDAS COMPLETADAS")
    print("="*80)
    print("\nRevisa los archivos en la carpeta output/")


if __name__ == "__main__":
    main()
