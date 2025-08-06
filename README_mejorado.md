# 🚀 HTML to Markdown Scraper - Versión Profesional

Extractor profesional de contenido HTML a Markdown usando Playwright con todas las mejores prácticas implementadas.

## ✨ Características Principales

### 🔧 **Mejoras Implementadas**
- ✅ **Configuración flexible** - Archivos JSON configurables
- ✅ **Manejo robusto de errores** - Try-catch en todas las operaciones
- ✅ **Logging profesional** - Logs detallados en archivo y consola
- ✅ **Validación completa** - Verificación de archivos y permisos
- ✅ **Optimización de recursos** - Reutilización inteligente del navegador
- ✅ **Estadísticas detalladas** - Métricas completas de procesamiento
- ✅ **Procesamiento paralelo** - Opción para URLs remotas
- ✅ **Nombres inteligentes** - Generación automática basada en contenido
- ✅ **Limpieza avanzada** - Eliminación inteligente de contenido excesivo
- ✅ **CLI avanzada** - Interfaz de línea de comandos completa
- ✅ **Reintentos automáticos** - Manejo de fallos temporales
- ✅ **Configuración por capas** - Sobrescritura flexible de opciones

## 📦 Instalación

### Paso 1: Instalar Dependencias
```bash
pip install playwright markdownify
playwright install
```

### Paso 2: Descargar el Script
Guarda el archivo `html_scraper_mejorado.py` en tu directorio de trabajo.

## 🚀 Uso Rápido

### 1. Crear Configuración de Ejemplo
```bash
python html_scraper_mejorado.py --create-config
```

### 2. Editar Configuración
Edita el archivo `config_ejemplo.json` generado con tus URLs y preferencias:

```json
{
  "urls": [
    "file:///C:/ruta/a/tu/archivo1.html",
    "file:///C:/ruta/a/tu/archivo2.html"
  ],
  "output_dir": "salida_markdown",
  "options": {
    "headless": true,
    "timeout": 30000,
    "parallel": false
  }
}
```

### 3. Ejecutar el Scraper
```bash
# Procesamiento secuencial (recomendado para archivos locales)
python html_scraper_mejorado.py --config config_ejemplo.json

# Procesamiento paralelo (para URLs remotas)
python html_scraper_mejorado.py --config config_ejemplo.json --parallel
```

## 🎯 Ejemplos de Uso

### Uso Básico con Configuración
```bash
python html_scraper_mejorado.py --config mi_config.json
```

### Sobrescribir URLs desde Línea de Comandos
```bash
python html_scraper_mejorado.py --urls "file:///archivo1.html" "file:///archivo2.html" --output "mi_salida"
```

### Modo Verbose para Debugging
```bash
python html_scraper_mejorado.py --config config.json --verbose
```

### Procesamiento Paralelo para URLs Remotas
```bash
python html_scraper_mejorado.py --config config.json --parallel
```

## ⚙️ Configuración Detallada

### Estructura del Archivo de Configuración

```json
{
  "urls": [
    "file:///ruta/local/archivo.html",
    "https://sitio-web.com/pagina"
  ],
  "output_dir": "salida_markdown",
  "options": {
    "headless": true,              // Navegador sin ventana
    "wait_until": "networkidle",   // Estrategia de espera
    "timeout": 30000,              // Timeout en milisegundos
    "parallel": false,             // Procesamiento paralelo
    "max_concurrent": 3,           // Máximo de tareas simultáneas
    "delay_between_requests": 1000, // Pausa entre requests (ms)
    "retry_attempts": 2            // Número de reintentos
  },
  "markdown": {
    "strip_elements": [            // Elementos HTML a remover
      "script", "style", "nav", "footer"
    ],
    "file_extension": ".md",       // Extensión de archivos de salida
    "naming_pattern": "contenido_{index}", // Patrón de nombres
    "smart_naming": true,          // Nombres basados en contenido URL
    "clean_excessive_whitespace": true // Limpieza de espacios
  },
  "logging": {
    "level": "INFO",               // Nivel de logging
    "console": true,               // Mostrar en consola
    "file": true,                  // Guardar en archivo
    "log_dir": "logs"              // Directorio de logs
  }
}
```

### Opciones de Wait Until
- `"load"` - Espera carga básica del HTML
- `"domcontentloaded"` - Espera construcción del DOM
- `"networkidle"` - Espera que no haya actividad de red (recomendado)

### Niveles de Logging
- `"DEBUG"` - Información muy detallada
- `"INFO"` - Información general (recomendado)
- `"WARNING"` - Solo advertencias y errores
- `"ERROR"` - Solo errores críticos

## 📊 Estadísticas y Monitoreo

El scraper genera estadísticas detalladas:

```
📊 ESTADÍSTICAS FINALES DEL PROCESAMIENTO
============================================================
📄 Total de archivos procesados: 5
✅ Exitosos: 4
❌ Fallidos: 1
📈 Tasa de éxito: 80.0%
📝 Total de palabras extraídas: 15,420
📏 Total de caracteres: 98,750
⏱️ Tiempo total: 45.32 segundos
⚡ Tiempo promedio por archivo: 11.33s
📊 Palabras promedio por archivo: 3,855
============================================================
```

Además, se guarda un archivo JSON con estadísticas completas en `estadisticas_procesamiento.json`.

## 🛠️ Características Avanzadas

### 1. **Manejo Inteligente de Errores**
- Reintentos automáticos en caso de fallos temporales
- Logging detallado de todos los errores
- Continuación del procesamiento aunque fallen algunos archivos

### 2. **Optimización de Recursos**
- Reutilización del navegador entre múltiples URLs
- Gestión eficiente de memoria
- Configuración de timeouts apropiados

### 3. **Nombres de Archivo Inteligentes**
Con `smart_naming: true`, los archivos se nombran basándose en el contenido de la URL:
- `archivo.html#introduccion` → `introduccion_01.md`
- `archivo.html#tema1` → `tema1_02.md`

### 4. **Validación Completa**
- Verificación de existencia de archivos locales
- Validación de permisos de escritura
- Comprobación de formato de configuración

### 5. **Procesamiento Paralelo**
Para URLs remotas, permite procesamiento simultáneo con control de concurrencia:
```bash
python html_scraper_mejorado.py --config config.json --parallel
```

## 🔧 Solución de Problemas

### Error: "playwright command not found"
```bash
pip install playwright
playwright install
```

### Error: "Permission denied"
Cambiar el directorio de salida a uno con permisos:
```json
{
  "output_dir": "~/Documents/markdown-files"
}
```

### Archivos Markdown vacíos
- Verificar que las URLs sean correctas
- Aumentar el timeout si las páginas tardan en cargar
- Usar `--verbose` para ver logs detallados

### Procesamiento muy lento
- Reducir `delay_between_requests`
- Cambiar `wait_until` a `"domcontentloaded"`
- Usar procesamiento paralelo para URLs remotas

## 📁 Estructura de Salida

```
salida_markdown/
├── introduccion_01.md
├── tema1_02.md
├── tema2_03.md
├── estadisticas_procesamiento.json
└── logs/
    └── scraper_20250105_143022.log
```

## 🤝 Contribuciones

Este es un script mejorado basado en código original. Las mejoras incluyen:

- Arquitectura orientada a objetos
- Configuración flexible
- Manejo robusto de errores
- Logging profesional
- Optimizaciones de rendimiento
- Interfaz de línea de comandos completa

## 📄 Licencia

Este código es una versión mejorada del script original con fines educativos y de mejora de herramientas de productividad.

---

¡Disfruta de tu herramienta de scraping profesional! 🎉