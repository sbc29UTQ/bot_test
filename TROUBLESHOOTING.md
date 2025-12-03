# Solución de Problemas

Esta guía te ayudará a resolver problemas comunes al instalar y usar el LinkedIn Profile Scraper.

## Error: Failed to build lxml

### Solución Rápida ✅

**El proyecto ya está configurado para funcionar sin lxml.** Simplemente instala las dependencias normalmente:

```bash
pip install -r requirements.txt
```

El scraper usará `html.parser` que viene incluido con Python y no requiere compilación.

### ¿Por qué ocurre este error?

`lxml` es una librería que requiere compiladores de C y otras dependencias del sistema para instalarse. En sistemas sin estas herramientas, la instalación falla.

### Si aún quieres usar lxml (opcional)

lxml es más rápido que html.parser, pero no es necesario. Si quieres usarlo:

#### En Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3-dev libxml2-dev libxslt1-dev zlib1g-dev
pip install lxml
```

#### En macOS:
```bash
brew install libxml2 libxslt
pip install lxml
```

#### En Windows:
```bash
# Instalar Visual C++ Build Tools desde:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Luego:
pip install lxml
```

#### Usar binarios precompilados:
```bash
pip install --only-binary lxml lxml
```

## Error: ChromeDriver not found

### Solución:

El proyecto usa `webdriver-manager` que descarga ChromeDriver automáticamente. Si hay problemas:

```bash
pip install --upgrade webdriver-manager
```

Si el problema persiste:

1. Verifica que Google Chrome esté instalado
2. Limpia el caché de webdriver-manager:

```bash
# Linux/Mac
rm -rf ~/.wdm

# Windows
# Elimina: C:\Users\TuUsuario\.wdm
```

## Error: Chrome binary not found

### Solución:

Instala Google Chrome:

- **Ubuntu/Debian:**
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
```

- **macOS:**
```bash
brew install --cask google-chrome
```

- **Windows:**
Descarga desde: https://www.google.com/chrome/

## Error: Permission denied al crear archivos

### Solución:

Asegúrate de que los directorios `data/` y `logs/` tengan permisos de escritura:

```bash
chmod 755 data logs
```

## No se encuentran perfiles

### Posibles causas y soluciones:

1. **Google detectó automatización:**
   - Reduce el número de páginas a procesar
   - Aumenta los delays entre peticiones
   - Ejecuta en modo no-headless para ver qué sucede

2. **Las keywords son muy específicas:**
   - Prueba con keywords más generales
   - Verifica la ortografía

3. **Bloqueado por CAPTCHA:**
   - Google puede mostrar CAPTCHAs si detecta comportamiento automatizado
   - Ejecuta en modo no-headless y resuelve el CAPTCHA manualmente
   - Espera unos minutos antes de volver a intentar

## Error: ImportError o ModuleNotFoundError

### Solución:

Asegúrate de estar en el entorno virtual correcto:

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

## El scraper es muy lento

### Soluciones:

1. **Usa modo headless:**
```python
scraper = LinkedInProfileScraper(headless=True)
```

2. **Reduce el número de páginas:**
```python
scraper.run(keywords="...", num_pages=1)  # Solo 1 página
```

3. **Optimiza las keywords:**
   - Sé más específico para obtener menos resultados pero más relevantes

## Error: Session not created

### Solución:

Actualiza las dependencias:

```bash
pip install --upgrade selenium webdriver-manager
```

O limpia el caché de ChromeDriver:

```bash
# Linux/Mac
rm -rf ~/.wdm

# Windows
# Elimina: C:\Users\TuUsuario\.wdm
```

## El navegador se cierra inmediatamente

### Solución:

Este comportamiento es normal al final de la ejecución. Si quieres mantener el navegador abierto para debugging:

```python
scraper = LinkedInProfileScraper(headless=False)
scraper.setup_driver()
scraper.search_google("python developer", num_pages=1)

# El navegador permanece abierto aquí
input("Presiona Enter para cerrar...")  # Espera input del usuario

scraper.close()
```

## Error: SSL Certificate verification failed

### Solución:

```bash
pip install --upgrade certifi
```

O temporalmente (no recomendado en producción):

```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

## Problemas con versiones de Python

### Solución:

Este proyecto requiere Python 3.8 o superior. Verifica tu versión:

```bash
python --version
```

Si es menor a 3.8, actualiza Python o usa pyenv:

```bash
# Con pyenv
pyenv install 3.11.0
pyenv local 3.11.0
```

## ¿Necesitas más ayuda?

Si ninguna de estas soluciones funciona:

1. Verifica los logs en la consola
2. Ejecuta en modo no-headless para ver qué sucede
3. Abre un issue en el repositorio con:
   - Sistema operativo y versión
   - Versión de Python
   - Error completo
   - Pasos para reproducir

## Tips de Rendimiento

### Optimizar velocidad:

```python
# Usa headless
scraper = LinkedInProfileScraper(headless=True)

# Configura timeouts más cortos (solo si tu conexión es buena)
chrome_options.add_argument("--page-load-strategy=eager")
```

### Evitar detección:

```python
# Agrega delays aleatorios entre peticiones
import random
import time

time.sleep(random.uniform(2, 5))
```

### Manejar grandes volúmenes:

```python
# Procesa keywords una por una y guarda resultados intermedios
keywords_list = ["python", "java", "javascript"]

for keyword in keywords_list:
    scraper = LinkedInProfileScraper(headless=True)
    scraper.run(keyword, num_pages=1)
    time.sleep(60)  # Espera entre búsquedas
```

---

Si encuentras otros problemas o soluciones, considera contribuir a este documento.
