"""
LinkedIn Profile Scraper
Busca perfiles de LinkedIn usando Google Search con Selenium y BeautifulSoup
"""

import time
import csv
import os
from datetime import datetime
from typing import List, Set
from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class LinkedInProfileScraper:
    """Scraper para encontrar perfiles de LinkedIn usando búsquedas en Google"""

    def __init__(self, headless: bool = False):
        """
        Inicializa el scraper

        Args:
            headless: Si True, ejecuta el navegador en modo headless (sin interfaz gráfica)
        """
        self.headless = headless
        self.driver = None
        self.profiles_found: Set[str] = set()

    def setup_driver(self):
        """Configura el driver de Selenium con Chrome"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

        print("✓ Driver configurado correctamente")

    def search_google(self, keywords: str, num_pages: int = 1):
        """
        Busca en Google con los keywords especificados

        Args:
            keywords: Keywords para buscar
            num_pages: Número de páginas de resultados a procesar
        """
        search_query = f"site:linkedin.com/in/ {keywords}"
        print(f"\n🔍 Buscando: {search_query}")

        self.driver.get("https://www.google.com")
        time.sleep(2)

        try:
            # Buscar el campo de búsqueda
            search_box = self.driver.find_element(By.NAME, "q")
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)

            # Procesar múltiples páginas de resultados
            for page in range(num_pages):
                print(f"\n📄 Procesando página {page + 1}/{num_pages}")
                self._extract_profiles_from_page()

                if page < num_pages - 1:
                    # Intentar ir a la siguiente página
                    if not self._go_to_next_page():
                        print("⚠ No hay más páginas de resultados")
                        break
                    time.sleep(3)

        except Exception as e:
            print(f"❌ Error durante la búsqueda: {str(e)}")

    def _extract_profiles_from_page(self):
        """Extrae URLs de perfiles de LinkedIn de la página actual"""
        try:
            # Obtener el HTML de la página
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')

            # Encontrar todos los enlaces en los resultados de búsqueda
            # Google usa diferentes estructuras, así que probamos varios selectores
            links = soup.find_all('a')

            profiles_in_page = 0
            for link in links:
                href = link.get('href', '')

                # Extraer URL limpia de LinkedIn
                if 'linkedin.com/in/' in href:
                    profile_url = self._clean_linkedin_url(href)

                    if profile_url and profile_url not in self.profiles_found:
                        self.profiles_found.add(profile_url)
                        profiles_in_page += 1
                        print(f"  ✓ Perfil encontrado: {profile_url}")

            print(f"  Total en esta página: {profiles_in_page}")

        except Exception as e:
            print(f"❌ Error extrayendo perfiles: {str(e)}")

    def _clean_linkedin_url(self, url: str) -> str:
        """
        Limpia y normaliza una URL de LinkedIn

        Args:
            url: URL potencialmente sucia de Google

        Returns:
            URL limpia de perfil de LinkedIn o cadena vacía
        """
        try:
            # Si la URL viene de Google, puede tener formato /url?q=...
            if '/url?q=' in url:
                parsed = parse_qs(urlparse(url).query)
                if 'q' in parsed:
                    url = parsed['q'][0]

            # Verificar que es una URL de perfil de LinkedIn
            if 'linkedin.com/in/' not in url:
                return ''

            # Extraer solo la parte relevante
            if 'linkedin.com/in/' in url:
                # Encontrar el inicio del perfil
                start = url.find('linkedin.com/in/')
                clean_url = 'https://' + url[start:]

                # Remover parámetros de URL
                if '?' in clean_url:
                    clean_url = clean_url.split('?')[0]

                # Remover trailing slash
                clean_url = clean_url.rstrip('/')

                return clean_url

        except Exception as e:
            print(f"⚠ Error limpiando URL {url}: {str(e)}")

        return ''

    def _go_to_next_page(self) -> bool:
        """
        Intenta navegar a la siguiente página de resultados

        Returns:
            True si se pudo ir a la siguiente página, False en caso contrario
        """
        try:
            # Buscar el botón "Siguiente" en Google
            next_button = self.driver.find_element(By.ID, "pnnext")
            next_button.click()
            return True
        except:
            try:
                # Método alternativo: buscar por texto
                next_link = self.driver.find_element(By.LINK_TEXT, "Siguiente")
                next_link.click()
                return True
            except:
                return False

    def save_results(self, filename: str = None):
        """
        Guarda los resultados en un archivo CSV

        Args:
            filename: Nombre del archivo (opcional, se genera automáticamente si no se provee)
        """
        if not self.profiles_found:
            print("\n⚠ No se encontraron perfiles para guardar")
            return

        # Crear directorio data si no existe
        os.makedirs('data', exist_ok=True)

        # Generar nombre de archivo si no se provee
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/linkedin_profiles_{timestamp}.csv"
        elif not filename.startswith('data/'):
            filename = f"data/{filename}"

        # Guardar en CSV
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Profile URL'])

                for profile in sorted(self.profiles_found):
                    writer.writerow([profile])

            print(f"\n✓ Resultados guardados en: {filename}")
            print(f"  Total de perfiles: {len(self.profiles_found)}")

        except Exception as e:
            print(f"❌ Error guardando resultados: {str(e)}")

    def close(self):
        """Cierra el driver de Selenium"""
        if self.driver:
            self.driver.quit()
            print("\n✓ Navegador cerrado")

    def run(self, keywords: List[str], num_pages: int = 1, output_file: str = None):
        """
        Ejecuta el scraper completo

        Args:
            keywords: Lista de keywords o una cadena de keywords
            num_pages: Número de páginas de resultados por búsqueda
            output_file: Nombre del archivo de salida (opcional)
        """
        try:
            print("=" * 60)
            print("LinkedIn Profile Scraper")
            print("=" * 60)

            self.setup_driver()

            # Convertir keywords a string si es una lista
            if isinstance(keywords, list):
                keywords = ' '.join(keywords)

            self.search_google(keywords, num_pages)

            print("\n" + "=" * 60)
            print(f"Búsqueda completada. Perfiles encontrados: {len(self.profiles_found)}")
            print("=" * 60)

            if self.profiles_found:
                self.save_results(output_file)

        except Exception as e:
            print(f"\n❌ Error durante la ejecución: {str(e)}")

        finally:
            self.close()


def main():
    """Función principal para ejecutar el scraper desde la línea de comandos"""
    # Ejemplo de uso
    scraper = LinkedInProfileScraper(headless=False)

    # Definir keywords de búsqueda
    keywords = "python developer"

    # Ejecutar búsqueda
    scraper.run(
        keywords=keywords,
        num_pages=2,  # Número de páginas de resultados de Google a procesar
        output_file="linkedin_profiles.csv"
    )


if __name__ == "__main__":
    main()
