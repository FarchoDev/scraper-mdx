# 📖 MANUAL DE USO: HTML to Markdown Scraper

## 🚀 Guía de Inicio Rápido

### ¿Qué hace este script?
Convierte archivos HTML locales a formato Markdown (.mdx) usando Playwright para navegar por los archivos y extraer su contenido completo, incluyendo contenido generado dinámicamente por JavaScript.

### ¿Cuándo usar esta herramienta?
- Convertir documentación HTML a Markdown
- Extraer contenido de cursos o tutoriales web offline
- Migrar contenido de formatos web a documentación técnica
- Procesar múltiples archivos HTML de forma automatizada

---

## 📋 Requisitos del Sistema

### **Requisitos Obligatorios:**
- **Python 3.7+** (verificar con `python --version`)
- **Sistema Operativo:** Windows, macOS, o Linux
- **Espacio en disco:** ~200MB para navegadores de Playwright
- **RAM:** Mínimo 4GB recomendado

### **Verificación de Requisitos:**
```bash
# Verificar Python
python --version
# o
python3 --version

# Verificar pip
pip --version
```

---

## ⚙️ Instalación Paso a Paso

### **Paso 1: Preparar el Entorno**
```bash
# Crear directorio para el proyecto
mkdir mi-html-scraper
cd mi-html-scraper

# [OPCIONAL] Crear entorno virtual (recomendado)
python -m venv scraper-env

# Activar entorno virtual
# En Windows:
scraper-env\Scripts\activate
# En macOS/Linux:
source scraper-env/bin/activate
```

### **Paso 2: Instalar Dependencias**
```bash
# Instalar paquetes Python requeridos
pip install playwright markdownify

# Instalar navegadores para Playwright (IMPORTANTE)
playwright install

# Verificar instalación
playwright --version
```

### **Paso 3: Preparar el Script**
```bash
# Copiar el código del script a un archivo
# Crear index.py con el contenido proporcionado
touch index.py
# (copiar el código completo al archivo)
```

---

## 🔧 Configuración Detallada

### **Configuración Básica: Variables Principales**

#### **1. Configurar URLs de Archivos**
```python
# EDITAR ESTAS RUTAS EN EL SCRIPT
URLS = [
    "file:///C:/ruta/a/tu/archivo1.html",
    "file:///C:/ruta/a/tu/archivo2.html",
    "file:///C:/ruta/a/tu/archivo3.html",
]
```

**📝 Formato de URLs:**
- **Windows:** `"file:///C:/Users/usuario/Documents/archivo.html"`
- **macOS:** `"file:///Users/usuario/Documents/archivo.html"`
- **Linux:** `"file:///home/usuario/documents/archivo.html"`

**⚠️ Puntos Importantes:**
- Usar barras `/` siempre, nunca `\`
- Incluir `file://` al inicio
- Rutas absolutas, no relativas
- Archivos deben existir en el sistema

#### **2. Configurar Directorio de Salida**
```python
# EDITAR ESTA RUTA EN EL SCRIPT
OUTPUT_DIR = "C:/Users/tu-usuario/Desktop/markdown-files"
```

**📁 Recomendaciones:**
- Usar ruta absoluta para mayor claridad
- Asegurar permisos de escritura
- El directorio se crea automáticamente si no existe

---

## 🎯 Guía de Uso Práctico

### **Uso Básico - Ejecutar el Script**
```bash
# Ejecutar desde la terminal/cmd
python index.py

# Si usas Python 3 específicamente
python3 index.py
```

### **Salida Esperada:**
```
Procesando archivo 1 / 5: file:///C:/ruta/archivo1.html
✅ Archivo guardado en: C:/salida/contenido_1.mdx
Procesando archivo 2 / 5: file:///C:/ruta/archivo2.html
✅ Archivo guardado en: C:/salida/contenido_2.mdx
...
```

---

## 🛠️ Personalización Avanzada

### **1. Cambiar Formato de Archivos de Salida**

#### **Cambiar a .md en lugar de .mdx:**
```python
# BUSCAR EN EL SCRIPT:
nombre_archivo = f"contenido_{i}.mdx"

# CAMBIAR A:
nombre_archivo = f"contenido_{i}.md"
```

#### **Nombres de archivo más descriptivos:**
```python
# En lugar de contenido_1.mdx, usar nombres basados en URL:
def generar_nombre_archivo(url, indice):
    # Extraer nombre del fragment (#introduccion, #tema1, etc.)
    if '#' in url:
        seccion = url.split('#')[-1]
        return f"{seccion}.mdx"
    else:
        return f"archivo_{indice}.mdx"

# Usar en main():
nombre_archivo = generar_nombre_archivo(ruta_local, i)
```

### **2. Filtrar Contenido Específico**

#### **Solo extraer secciones específicas:**
```python
def filtrar_contenido_principal(html_content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Ejemplo: Solo contenido de <main> o <article>
    contenido_principal = soup.find('main') or soup.find('article')
    
    if contenido_principal:
        return str(contenido_principal)
    else:
        return html_content

# Modificar en extraer_contenido():
content = await page.content()
content = filtrar_contenido_principal(content)  # AGREGAR ESTA LÍNEA
```

### **3. Configuración de Playwright Avanzada**

#### **Cambiar navegador o configuraciones:**
```python
async def extraer_contenido(playwright, ruta_local):
    # Opciones de navegador
    browser = await playwright.chromium.launch(
        headless=True,      # False para ver navegador
        slow_mo=1000       # Delay entre acciones (ms)
    )
    
    # Configurar contexto con opciones adicionales
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
```

#### **Manejar páginas con autenticación:**
```python
context = await browser.new_context(
    extra_http_headers={
        'Authorization': 'Bearer tu-token-aqui'
    }
)
```

---

## 🔧 Extensiones y Modificaciones

### **Extensión 1: Procesamiento de URLs Remotas**
```python
# Cambiar URLS para páginas web:
URLS = [
    "https://docs.python.org/3/tutorial/",
    "https://docs.python.org/3/library/",
]

# Agregar manejo de rate limiting:
import time

async def extraer_contenido_con_delay(playwright, ruta_local):
    time.sleep(2)  # Esperar 2 segundos entre requests
    # ... resto del código igual
```

### **Extensión 2: Configuración desde Archivo JSON**
```python
# Crear config.json:
{
  "urls": [
    "file:///C:/archivo1.html",
    "file:///C:/archivo2.html"
  ],
  "output_dir": "C:/salida",
  "options": {
    "headless": true,
    "wait_until": "networkidle"
  }
}

# Modificar script para leer configuración:
import json

def cargar_configuracion():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# En main():
config = cargar_configuracion()
URLS = config['urls']
OUTPUT_DIR = config['output_dir']
```

### **Extensión 3: Logging Detallado**
```python
import logging
from datetime import datetime

# Configurar logging al inicio del script:
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'scraper_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

# Reemplazar print() con logging:
logging.info(f"Procesando archivo {i} / {len(URLS)}: {ruta_local}")
logging.info(f"Archivo guardado en: {ruta_archivo}")
```

---

## 🚨 Solución de Problemas Comunes

### **Error: "playwright command not found"**
```bash
# Solución:
pip install playwright
playwright install
```

### **Error: "Permission denied" al guardar archivos**
```python
# Cambiar OUTPUT_DIR a directorio con permisos:
OUTPUT_DIR = os.path.expanduser("~/Documents/markdown-files")
```

### **Error: "No such file or directory" para archivos HTML**
```bash
# Verificar que archivo existe:
ls -la /ruta/a/tu/archivo.html

# Para Windows:
dir C:\ruta\a\tu\archivo.html
```

### **El script se cuelga o es muy lento**
```python
# Cambiar wait_until para carga más rápida:
await page.goto(ruta_local, wait_until="domcontentloaded")

# O agregar timeout:
await page.goto(ruta_local, wait_until="networkidle", timeout=10000)
```

### **Archivos Markdown vacíos o mal formateados**
```python
# Verificar contenido antes de convertir:
if not html_content or len(html_content) < 100:
    print(f"⚠️ Contenido sospechosamente corto en {ruta_local}")
    
# Ajustar opciones de markdownify:
markdown = md(html_content, 
    strip=['script', 'style', 'nav', 'header', 'footer'],
    convert=['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'a']
)
```

---

## 📊 Casos de Uso Específicos

### **Caso 1: Procesar Documentación Técnica**
```python
# Para documentación con código:
markdown = md(html_content, 
    strip=['script', 'style'],
    code_language='python'  # Especificar lenguaje por defecto
)
```

### **Caso 2: Procesar Contenido Educativo**
```python
# Mantener estructura de tablas y listas:
markdown = md(html_content,
    strip=['script', 'style', 'nav'],
    convert=['p', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th']
)
```

### **Caso 3: Procesar Solo Texto Principal**
```python
def extraer_solo_texto(html_content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remover navegación, sidebars, etc.
    for elemento in soup(['nav', 'sidebar', 'footer', 'header', 'aside']):
        elemento.decompose()
    
    # Buscar contenido principal
    main_content = (soup.find('main') or 
                   soup.find('article') or 
                   soup.find(class_='content') or
                   soup.find(id='content'))
    
    return str(main_content) if main_content else str(soup)
```

---

## 📈 Métricas y Monitoreo

### **Agregar Contador de Palabras y Tiempo**
```python
import time
from datetime import datetime

def contar_palabras(texto):
    return len(texto.split())

# En main():
inicio = time.time()
total_palabras = 0

for i, ruta_local in enumerate(URLS, start=1):
    # ... proceso normal ...
    palabras = contar_palabras(markdown)
    total_palabras += palabras
    print(f"✅ Archivo {i}: {palabras} palabras")

fin = time.time()
print(f"\n📊 Resumen:")
print(f"   Archivos procesados: {len(URLS)}")
print(f"   Total palabras: {total_palabras:,}")
print(f"   Tiempo total: {fin-inicio:.2f} segundos")
```

---

## 🎓 Consejos de Mejores Prácticas

### **1. Antes de Ejecutar**
- [ ] Verificar que todos los archivos HTML existen
- [ ] Confirmar permisos de escritura en directorio de salida
- [ ] Hacer backup de archivos importantes
- [ ] Probar con un archivo pequeño primero

### **2. Durante la Ejecución**
- [ ] Monitorear uso de memoria (Playwright consume recursos)
- [ ] No interrumpir el proceso a menos que sea necesario  
- [ ] Verificar logs de errores regularmente

### **3. Después de la Ejecución**
- [ ] Revisar archivos generados manualmente
- [ ] Verificar que el contenido se convirtió correctamente
- [ ] Hacer limpieza de archivos temporales si los hay

### **4. Para Uso en Producción**
- [ ] Implementar manejo robusto de errores
- [ ] Agregar tests automatizados
- [ ] Configurar logging detallado
- [ ] Documentar configuraciones específicas

---

## 📞 Soporte y Recursos Adicionales

### **Documentación de Dependencias:**
- **Playwright:** https://playwright.dev/python/docs/intro
- **Markdownify:** https://pypi.org/project/markdownify/
- **BeautifulSoup (opcional):** https://www.crummy.com/software/BeautifulSoup/

### **Comandos de Diagnóstico:**
```bash
# Verificar instalación de Playwright
playwright --version

# Listar navegadores instalados
playwright show-browsers

# Verificar paquetes Python
pip list | grep -E "(playwright|markdownify)"
```

Este manual te proporciona todo lo necesario para usar, personalizar y mantener el script de conversión HTML a Markdown. ¡Experimenta con las diferentes opciones para adaptarlo a tus necesidades específicas!