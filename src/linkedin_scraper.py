"""
LinkedIn Profile Scraper - Paradigma Funcional
Busca perfiles de LinkedIn usando Google Search con keywords específicas
"""

import time
import os
from datetime import datetime
from typing import List, Set, Dict, Tuple, Optional
from urllib.parse import urlparse, parse_qs
from functools import reduce

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


# =============================================================================
# TIPOS Y CONFIGURACIÓN
# =============================================================================

ScraperConfig = Dict[str, any]
ProfileData = Dict[str, str]
ScraperState = Dict[str, any]


def create_config(headless: bool = False, debug: bool = False,
                  num_pages: int = 1, wait_time: int = 5) -> ScraperConfig:
    """
    Crea una configuración para el scraper.

    Args:
        headless: Ejecutar navegador sin interfaz gráfica
        debug: Mostrar información de depuración
        num_pages: Número de páginas a procesar
        wait_time: Tiempo de espera en segundos

    Returns:
        Diccionario de configuración
    """
    return {
        'headless': headless,
        'debug': debug,
        'num_pages': num_pages,
        'wait_time': wait_time,
    }


def create_initial_state() -> ScraperState:
    """
    Crea el estado inicial del scraper.

    Returns:
        Diccionario con estado inicial
    """
    return {
        'profiles_data': [],
        'profiles_urls': set(),
        'driver': None,
    }


# =============================================================================
# FUNCIONES DE DRIVER
# =============================================================================

def setup_chrome_options(headless: bool) -> Options:
    """
    Configura las opciones de Chrome.
    Función pura que no tiene efectos secundarios.

    Args:
        headless: Si True, modo sin interfaz gráfica

    Returns:
        Opciones de Chrome configuradas
    """
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    return chrome_options


def create_driver(config: ScraperConfig) -> webdriver.Chrome:
    """
    Crea y configura un driver de Chrome.

    Args:
        config: Configuración del scraper

    Returns:
        Driver de Chrome configurado
    """
    chrome_options = setup_chrome_options(config['headless'])
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)

    print("✓ Driver configurado correctamente")
    return driver


def close_driver(driver: Optional[webdriver.Chrome]) -> None:
    """
    Cierra el driver de forma segura.

    Args:
        driver: Driver a cerrar
    """
    if driver:
        driver.quit()
        print("\n✓ Navegador cerrado")


# =============================================================================
# FUNCIONES DE BÚSQUEDA
# =============================================================================

def build_search_query(keywords: List[str]) -> str:
    """
    Construye la query de búsqueda para Google.
    Función pura que transforma datos.

    Args:
        keywords: Lista de keywords

    Returns:
        Query de búsqueda formateada

    Ejemplo:
        >>> build_search_query(["Director de Marketing", "Perú"])
        'site:linkedin.com/in "Director de Marketing" "Perú"'
    """
    def add_quotes(keyword: str) -> str:
        """Agrega comillas a una keyword si no las tiene."""
        if keyword.startswith('"') and keyword.endswith('"'):
            return keyword
        return f'"{keyword}"'

    quoted_keywords = map(add_quotes, keywords)
    query_parts = ["site:linkedin.com/in"] + list(quoted_keywords)

    return " ".join(query_parts)


def perform_search(driver: webdriver.Chrome, query: str, wait_time: int,
                   debug: bool) -> None:
    """
    Realiza una búsqueda en Google.

    Args:
        driver: Driver de Chrome
        query: Query de búsqueda
        wait_time: Tiempo de espera en segundos
        debug: Mostrar información de debug
    """
    driver.get("https://www.google.com")
    time.sleep(2)

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    if debug:
        print(f"[DEBUG] Esperando {wait_time}s a que carguen los resultados...")
    time.sleep(wait_time)


def navigate_to_next_page(driver: webdriver.Chrome) -> bool:
    """
    Intenta navegar a la siguiente página de resultados.

    Args:
        driver: Driver de Chrome

    Returns:
        True si se pudo navegar, False en caso contrario
    """
    try:
        next_button = driver.find_element(By.ID, "pnnext")
        next_button.click()
        return True
    except:
        try:
            next_link = driver.find_element(By.LINK_TEXT, "Siguiente")
            next_link.click()
            return True
        except:
            return False


# =============================================================================
# FUNCIONES DE EXTRACCIÓN
# =============================================================================

def clean_linkedin_url(url: str) -> Optional[str]:
    """
    Limpia y normaliza una URL de LinkedIn.
    Función pura que transforma datos.

    Args:
        url: URL potencialmente sucia

    Returns:
        URL limpia o None
    """
    try:
        # Extraer URL de parámetro de Google
        if '/url?q=' in url:
            parsed = parse_qs(urlparse(url).query)
            if 'q' in parsed:
                url = parsed['q'][0]

        # Verificar que es una URL de perfil de LinkedIn
        if 'linkedin.com/in/' not in url:
            return None

        # Extraer la parte relevante
        start = url.find('linkedin.com/in/')
        clean_url = 'https://' + url[start:]

        # Remover parámetros y trailing slash
        clean_url = clean_url.split('?')[0].rstrip('/')

        return clean_url
    except:
        return None


def extract_profile_from_link(link, profiles_urls: Set[str]) -> Optional[ProfileData]:
    """
    Extrae información de perfil de un elemento link.

    Args:
        link: Elemento BeautifulSoup del enlace
        profiles_urls: Set de URLs ya procesadas

    Returns:
        Diccionario con datos del perfil o None
    """
    href = link.get('href', '')

    if 'linkedin.com/in/' not in href:
        return None

    profile_url = clean_linkedin_url(href)

    if not profile_url or profile_url in profiles_urls:
        return None

    # Extraer título
    title = link.get_text(strip=True)
    if not title:
        parent = link.find_parent()
        if parent:
            h3_tag = parent.find('h3')
            title = h3_tag.get_text(strip=True) if h3_tag else "Sin título"

    return {
        'url': profile_url,
        'title': title if title else "Sin título",
        'snippet': ""
    }


def extract_profile_from_result(result, profiles_urls: Set[str]) -> Optional[ProfileData]:
    """
    Extrae información de perfil de un resultado de búsqueda.

    Args:
        result: Elemento BeautifulSoup del resultado
        profiles_urls: Set de URLs ya procesadas

    Returns:
        Diccionario con datos del perfil o None
    """
    link_tag = result.find('a', href=True)
    if not link_tag:
        return None

    href = link_tag.get('href', '')

    if 'linkedin.com/in/' not in href:
        return None

    profile_url = clean_linkedin_url(href)

    if not profile_url or profile_url in profiles_urls:
        return None

    # Extraer título
    title_tag = result.find('h3')
    title = title_tag.get_text(strip=True) if title_tag else "Sin título"

    # Extraer snippet
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

    return {
        'url': profile_url,
        'title': title,
        'snippet': snippet
    }


def find_results_with_selectors(soup: BeautifulSoup, debug: bool) -> List:
    """
    Busca resultados usando múltiples selectores CSS.

    Args:
        soup: Objeto BeautifulSoup
        debug: Mostrar información de debug

    Returns:
        Lista de elementos encontrados
    """
    selectors = [
        ('div', 'g'),
        ('div', 'Gx5Zad'),
        ('div', 'kvH3mc'),
        ('div', 'egMi0'),
    ]

    search_results = []
    for tag, class_name in selectors:
        results = soup.find_all(tag, class_=class_name)
        if results:
            search_results.extend(results)
            if debug:
                print(f"[DEBUG] Encontrados {len(results)} resultados con {tag}.{class_name}")

    return search_results


def extract_profiles_strategy_1(soup: BeautifulSoup, profiles_urls: Set[str],
                                 debug: bool) -> List[ProfileData]:
    """
    Estrategia 1: Usar selectores CSS específicos.

    Args:
        soup: Objeto BeautifulSoup
        profiles_urls: Set de URLs ya procesadas
        debug: Mostrar información de debug

    Returns:
        Lista de perfiles encontrados
    """
    search_results = find_results_with_selectors(soup, debug)

    if not search_results:
        return []

    profiles = []
    for result in search_results:
        profile = extract_profile_from_result(result, profiles_urls)
        if profile:
            profiles.append(profile)
            profiles_urls.add(profile['url'])

    return profiles


def extract_profiles_strategy_2(soup: BeautifulSoup, profiles_urls: Set[str],
                                 debug: bool) -> List[ProfileData]:
    """
    Estrategia 2: Buscar todos los enlaces y filtrar.

    Args:
        soup: Objeto BeautifulSoup
        profiles_urls: Set de URLs ya procesadas
        debug: Mostrar información de debug

    Returns:
        Lista de perfiles encontrados
    """
    if debug:
        print("[DEBUG] Buscando todos los enlaces en la página...")

    all_links = soup.find_all('a', href=True)

    profiles = []
    for link in all_links:
        profile = extract_profile_from_link(link, profiles_urls)
        if profile:
            profiles.append(profile)
            profiles_urls.add(profile['url'])

    return profiles


def extract_profiles_from_page(driver: webdriver.Chrome, state: ScraperState,
                                config: ScraperConfig) -> ScraperState:
    """
    Extrae perfiles de la página actual.
    Función que actualiza el estado del scraper.

    Args:
        driver: Driver de Chrome
        state: Estado actual del scraper
        config: Configuración del scraper

    Returns:
        Estado actualizado
    """
    try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        if config['debug']:
            print("\n[DEBUG] Analizando página...")
            with open('debug_page.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
            print("[DEBUG] HTML guardado en debug_page.html")

        profiles_urls = state['profiles_urls'].copy()

        # Estrategia 1: Selectores CSS
        profiles = extract_profiles_strategy_1(soup, profiles_urls, config['debug'])

        # Estrategia 2: Todos los enlaces (si estrategia 1 no funcionó)
        if not profiles:
            if config['debug']:
                print("[DEBUG] No se encontraron con selectores, probando estrategia 2...")
            profiles = extract_profiles_strategy_2(soup, profiles_urls, config['debug'])

        # Imprimir resultados
        for profile in profiles:
            print(f"  ✓ Perfil encontrado: {profile['url']}")
            if profile['title'] != "Sin título":
                print(f"    Título: {profile['title']}")

        print(f"  Total en esta página: {len(profiles)}")

        if not profiles and config['debug']:
            print("\n[DEBUG] ⚠️ No se encontraron perfiles")
            print("[DEBUG] Verifica debug_page.html")

        # Actualizar estado
        return {
            **state,
            'profiles_data': state['profiles_data'] + profiles,
            'profiles_urls': profiles_urls
        }

    except Exception as e:
        print(f"❌ Error extrayendo perfiles: {str(e)}")
        if config['debug']:
            import traceback
            traceback.print_exc()
        return state


# =============================================================================
# FUNCIONES DE GUARDADO
# =============================================================================

def format_profile_entry(profile: ProfileData, index: int) -> str:
    """
    Formatea un perfil para el archivo TXT.
    Función pura que transforma datos.

    Args:
        profile: Datos del perfil
        index: Número del perfil

    Returns:
        String formateado
    """
    lines = [
        f"PERFIL #{index}",
        "-" * 80,
        f"URL: {profile['url']}"
    ]

    if profile['title'] and profile['title'] != "Sin título":
        lines.append(f"Título: {profile['title']}")

    if profile['snippet']:
        lines.append(f"Descripción: {profile['snippet']}")

    lines.append("")

    return "\n".join(lines)


def format_output(profiles: List[ProfileData], keywords: List[str]) -> str:
    """
    Formatea la salida completa del archivo TXT.
    Función pura que transforma datos.

    Args:
        profiles: Lista de perfiles
        keywords: Keywords de búsqueda

    Returns:
        String con el contenido completo del archivo
    """
    lines = [
        "=" * 80,
        "PERFILES DE LINKEDIN ENCONTRADOS",
        "=" * 80,
        "",
        f"Búsqueda realizada: {build_search_query(keywords)}",
        f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total de perfiles encontrados: {len(profiles)}",
        "",
        "=" * 80,
        ""
    ]

    # Agregar cada perfil
    profile_entries = [
        format_profile_entry(profile, i + 1)
        for i, profile in enumerate(profiles)
    ]
    lines.extend(profile_entries)

    # Agregar resumen de URLs
    lines.extend([
        "",
        "=" * 80,
        "RESUMEN - SOLO URLs",
        "=" * 80,
        ""
    ])

    urls = [profile['url'] for profile in profiles]
    lines.extend(urls)

    return "\n".join(lines)


def save_results_to_file(profiles: List[ProfileData], keywords: List[str],
                         filename: Optional[str] = None) -> str:
    """
    Guarda los resultados en un archivo TXT.

    Args:
        profiles: Lista de perfiles
        keywords: Keywords de búsqueda
        filename: Nombre del archivo (opcional)

    Returns:
        Ruta del archivo guardado
    """
    if not profiles:
        print("\n⚠ No se encontraron perfiles para guardar")
        return ""

    os.makedirs('output', exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/linkedin_profiles_{timestamp}.txt"
    elif not filename.startswith('output/'):
        filename = f"output/{filename}"

    try:
        content = format_output(profiles, keywords)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n✓ Resultados guardados en: {filename}")
        print(f"  Total de perfiles: {len(profiles)}")

        return filename
    except Exception as e:
        print(f"❌ Error guardando resultados: {str(e)}")
        return ""


# =============================================================================
# FUNCIÓN PRINCIPAL DE COMPOSICIÓN
# =============================================================================

def scrape_linkedin_profiles(keywords: List[str], config: Optional[ScraperConfig] = None,
                              output_file: Optional[str] = None) -> ScraperState:
    """
    Función principal que compone todas las operaciones del scraper.
    Paradigma funcional: composición de funciones.

    Args:
        keywords: Lista de keywords para buscar
        config: Configuración del scraper (opcional)
        output_file: Nombre del archivo de salida (opcional)

    Returns:
        Estado final del scraper con todos los perfiles encontrados
    """
    # Configuración por defecto
    if config is None:
        config = create_config()

    # Estado inicial
    state = create_initial_state()
    driver = None

    try:
        print("=" * 80)
        print("LinkedIn Profile Scraper - Paradigma Funcional")
        print("=" * 80)

        # Crear driver
        driver = create_driver(config)
        state['driver'] = driver

        # Construir query
        query = build_search_query(keywords)
        print(f"\n🔍 Búsqueda: {query}")

        # Realizar búsqueda
        perform_search(driver, query, config['wait_time'], config['debug'])

        # Procesar páginas
        for page in range(config['num_pages']):
            print(f"\n📄 Procesando página {page + 1}/{config['num_pages']}")

            # Extraer perfiles (función pura que retorna nuevo estado)
            state = extract_profiles_from_page(driver, state, config)

            # Navegar a siguiente página si es necesario
            if page < config['num_pages'] - 1:
                if not navigate_to_next_page(driver):
                    print("⚠ No hay más páginas de resultados")
                    break
                time.sleep(3)

        # Mostrar resumen
        print("\n" + "=" * 80)
        print(f"Búsqueda completada. Perfiles encontrados: {len(state['profiles_data'])}")
        print("=" * 80)

        # Guardar resultados
        if state['profiles_data']:
            save_results_to_file(state['profiles_data'], keywords, output_file)

        return state

    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {str(e)}")
        if config['debug']:
            import traceback
            traceback.print_exc()
        return state

    finally:
        close_driver(driver)


# =============================================================================
# FUNCIÓN AUXILIAR PARA COMPATIBILIDAD
# =============================================================================

def run_scraper(keywords: List[str], num_pages: int = 1,
                output_file: Optional[str] = None, headless: bool = False,
                debug: bool = False) -> List[ProfileData]:
    """
    Función auxiliar simplificada para ejecutar el scraper.

    Args:
        keywords: Lista de keywords
        num_pages: Número de páginas a procesar
        output_file: Nombre del archivo de salida
        headless: Modo sin interfaz gráfica
        debug: Modo debug

    Returns:
        Lista de perfiles encontrados
    """
    config = create_config(headless=headless, debug=debug, num_pages=num_pages)
    state = scrape_linkedin_profiles(keywords, config, output_file)
    return state['profiles_data']


if __name__ == "__main__":
    # Ejemplo de uso
    keywords = ["Director de Marketing Digital", "Perú"]
    config = create_config(headless=False, debug=True, num_pages=2)

    result = scrape_linkedin_profiles(keywords, config, "marketing_peru.txt")
    print(f"\n✅ Perfiles encontrados: {len(result['profiles_data'])}")
