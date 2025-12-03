"""
LinkedIn Profile Scraper
Busca perfiles de LinkedIn usando Google Search con keywords específicas
"""

import time
import os
from datetime import datetime
from typing import List, Set, Dict
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

    def __init__(self, headless: bool = False, debug: bool = False):
        """
        Inicializa el scraper

        Args:
            headless: Si True, ejecuta el navegador en modo headless (sin interfaz gráfica)
            debug: Si True, muestra información de depuración
        """
        self.headless = headless
        self.debug = debug
        self.driver = None
        self.profiles_data: List[Dict] = []
        self.profiles_urls: Set[str] = set()

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

    def build_search_query(self, keywords: List[str]) -> str:
        """
        Construye la query de búsqueda para Google

        Args:
            keywords: Lista de keywords. Elementos con espacios se pondrán entre comillas

        Returns:
            Query de búsqueda formateada

        Ejemplo:
            keywords = ["Director de Marketing Digital", "Perú"]
            resultado = 'site:linkedin.com/in "Director de Marketing Digital" "Perú"'
        """
        # Comenzar con site:linkedin.com/in
        query_parts = ["site:linkedin.com/in"]

        # Agregar cada keyword entre comillas
        for keyword in keywords:
            # Si la keyword ya tiene comillas, usarla tal cual
            if keyword.startswith('"') and keyword.endswith('"'):
                query_parts.append(keyword)
            else:
                # Poner entre comillas
                query_parts.append(f'"{keyword}"')

        return " ".join(query_parts)

    def search_google(self, keywords: List[str], num_pages: int = 1):
        """
        Busca en Google con los keywords especificados

        Args:
            keywords: Lista de keywords para la búsqueda
            num_pages: Número de páginas de resultados a procesar
        """
        search_query = self.build_search_query(keywords)
        print(f"\n🔍 Búsqueda: {search_query}")

        self.driver.get("https://www.google.com")
        time.sleep(2)

        try:
            # Buscar el campo de búsqueda
            search_box = self.driver.find_element(By.NAME, "q")
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)

            # Esperar a que cargue la página de resultados
            if self.debug:
                print("[DEBUG] Esperando a que carguen los resultados...")
            time.sleep(5)  # Aumentar el tiempo de espera

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
        """Extrae URLs y títulos de perfiles de LinkedIn de la página actual"""
        try:
            # Obtener el HTML de la página
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            if self.debug:
                print("\n[DEBUG] Analizando página...")
                # Guardar HTML para depuración
                with open('debug_page.html', 'w', encoding='utf-8') as f:
                    f.write(page_source)
                print("[DEBUG] HTML guardado en debug_page.html")

            # Estrategia 1: Buscar en divs con diferentes clases que Google usa
            search_results = []

            # Probar diferentes selectores que Google usa
            selectors = [
                ('div', 'g'),           # Selector clásico
                ('div', 'Gx5Zad'),      # Selector alternativo
                ('div', 'kvH3mc'),      # Otro selector de Google
                ('div', 'egMi0'),       # Nuevo selector
            ]

            for tag, class_name in selectors:
                results = soup.find_all(tag, class_=class_name)
                if results:
                    search_results.extend(results)
                    if self.debug:
                        print(f"[DEBUG] Encontrados {len(results)} resultados con selector {tag}.{class_name}")

            # Estrategia 2: Si no encontramos resultados con selectores específicos,
            # buscar TODOS los enlaces en la página
            if not search_results:
                if self.debug:
                    print("[DEBUG] No se encontraron resultados con selectores específicos")
                    print("[DEBUG] Buscando todos los enlaces en la página...")

                # Buscar todos los enlaces directamente
                all_links = soup.find_all('a', href=True)

                profiles_in_page = 0
                for link in all_links:
                    href = link.get('href', '')

                    # Filtrar solo enlaces de LinkedIn
                    if 'linkedin.com/in/' in href:
                        profile_url = self._clean_linkedin_url(href)

                        if profile_url and profile_url not in self.profiles_urls:
                            # Intentar obtener el texto del enlace o del elemento padre
                            title = link.get_text(strip=True)

                            # Si el título está vacío, buscar en el elemento padre
                            if not title:
                                parent = link.find_parent()
                                if parent:
                                    h3_tag = parent.find('h3')
                                    title = h3_tag.get_text(strip=True) if h3_tag else "Sin título"

                            # Guardar información del perfil
                            profile_data = {
                                'url': profile_url,
                                'title': title if title else "Sin título",
                                'snippet': ""
                            }

                            self.profiles_data.append(profile_data)
                            self.profiles_urls.add(profile_url)
                            profiles_in_page += 1

                            print(f"  ✓ Perfil encontrado: {profile_url}")
                            if title and title != "Sin título":
                                print(f"    Título: {title}")

                print(f"  Total en esta página: {profiles_in_page}")
                return

            # Estrategia 3: Procesar los resultados encontrados con selectores específicos
            profiles_in_page = 0
            for result in search_results:
                try:
                    # Buscar el enlace en el resultado
                    link_tag = result.find('a', href=True)
                    if not link_tag:
                        continue

                    href = link_tag.get('href', '')

                    # Extraer URL limpia de LinkedIn
                    if 'linkedin.com/in/' in href:
                        profile_url = self._clean_linkedin_url(href)

                        if profile_url and profile_url not in self.profiles_urls:
                            # Intentar extraer el título/nombre del resultado
                            title_tag = result.find('h3')
                            title = title_tag.get_text(strip=True) if title_tag else "Sin título"

                            # Intentar extraer el snippet/descripción
                            snippet = ""
                            snippet_selectors = [
                                ('div', 'VwiC3b'),
                                ('span', 'aCOpRe'),
                                ('div', 'IsZvec'),
                                ('div', 's3v9rd'),
                            ]

                            for tag, class_name in snippet_selectors:
                                snippet_tag = result.find(tag, class_=class_name)
                                if snippet_tag:
                                    snippet = snippet_tag.get_text(strip=True)
                                    break

                            # Guardar información del perfil
                            profile_data = {
                                'url': profile_url,
                                'title': title,
                                'snippet': snippet
                            }

                            self.profiles_data.append(profile_data)
                            self.profiles_urls.add(profile_url)
                            profiles_in_page += 1

                            print(f"  ✓ Perfil encontrado: {profile_url}")
                            if title != "Sin título":
                                print(f"    Título: {title}")

                except Exception as e:
                    if self.debug:
                        print(f"[DEBUG] Error procesando resultado: {str(e)}")
                    continue

            print(f"  Total en esta página: {profiles_in_page}")

            if profiles_in_page == 0 and self.debug:
                print("\n[DEBUG] ⚠️ No se encontraron perfiles")
                print("[DEBUG] Verifica debug_page.html para ver el HTML de la página")

        except Exception as e:
            print(f"❌ Error extrayendo perfiles: {str(e)}")
            if self.debug:
                import traceback
                print(f"[DEBUG] Traceback completo:")
                traceback.print_exc()

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

    def save_results_txt(self, filename: str = None, search_keywords: List[str] = None):
        """
        Guarda los resultados en un archivo TXT

        Args:
            filename: Nombre del archivo (opcional, se genera automáticamente si no se provee)
            search_keywords: Keywords de búsqueda para incluir en el archivo
        """
        if not self.profiles_data:
            print("\n⚠ No se encontraron perfiles para guardar")
            return

        # Crear directorio output si no existe
        os.makedirs('output', exist_ok=True)

        # Generar nombre de archivo si no se provee
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/linkedin_profiles_{timestamp}.txt"
        elif not filename.startswith('output/'):
            filename = f"output/{filename}"

        # Guardar en TXT
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Escribir encabezado
                f.write("=" * 80 + "\n")
                f.write("PERFILES DE LINKEDIN ENCONTRADOS\n")
                f.write("=" * 80 + "\n\n")

                # Escribir información de búsqueda
                if search_keywords:
                    f.write(f"Búsqueda realizada: {self.build_search_query(search_keywords)}\n")

                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total de perfiles encontrados: {len(self.profiles_data)}\n")
                f.write("\n" + "=" * 80 + "\n\n")

                # Escribir cada perfil
                for i, profile in enumerate(self.profiles_data, 1):
                    f.write(f"PERFIL #{i}\n")
                    f.write("-" * 80 + "\n")
                    f.write(f"URL: {profile['url']}\n")

                    if profile['title'] and profile['title'] != "Sin título":
                        f.write(f"Título: {profile['title']}\n")

                    if profile['snippet']:
                        f.write(f"Descripción: {profile['snippet']}\n")

                    f.write("\n")

                # Escribir resumen de URLs al final
                f.write("\n" + "=" * 80 + "\n")
                f.write("RESUMEN - SOLO URLs\n")
                f.write("=" * 80 + "\n\n")

                for profile in self.profiles_data:
                    f.write(f"{profile['url']}\n")

            print(f"\n✓ Resultados guardados en: {filename}")
            print(f"  Total de perfiles: {len(self.profiles_data)}")

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
            keywords: Lista de keywords para la búsqueda
            num_pages: Número de páginas de resultados por búsqueda
            output_file: Nombre del archivo de salida (opcional)
        """
        try:
            print("=" * 80)
            print("LinkedIn Profile Scraper")
            print("=" * 80)

            self.setup_driver()
            self.search_google(keywords, num_pages)

            print("\n" + "=" * 80)
            print(f"Búsqueda completada. Perfiles encontrados: {len(self.profiles_data)}")
            print("=" * 80)

            if self.profiles_data:
                self.save_results_txt(output_file, keywords)

        except Exception as e:
            print(f"\n❌ Error durante la ejecución: {str(e)}")

        finally:
            self.close()


def main():
    """Función principal para ejecutar el scraper desde la línea de comandos"""
    # Ejemplo de uso
    scraper = LinkedInProfileScraper(headless=False)

    # Ejemplo 1: Director de Marketing Digital en Perú
    keywords = [
        "Director de Marketing Digital",
        "Perú"
    ]

    # Ejecutar búsqueda
    scraper.run(
        keywords=keywords,
        num_pages=2,
        output_file="marketing_peru.txt"
    )


if __name__ == "__main__":
    main()
