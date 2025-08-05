# 📚 GLOSARIO DE TÉRMINOS TÉCNICOS

## Términos de Programación Python

### **asyncio**
Biblioteca nativa de Python para programación asíncrona. Permite ejecutar múltiples operaciones concurrentemente sin bloquear el hilo principal.
- **Ejemplo:** `await asyncio.sleep(1)` pausa la ejecución sin bloquear otras tareas.

### **async/await**
Sintaxis de Python para definir y llamar funciones asíncronas.
- **async def:** Define una función asíncrona
- **await:** Pausa la ejecución hasta que se complete una operación asíncrona

### **Context Manager**
Patrón que garantiza la correcta limpieza de recursos usando `with` o `async with`.
- **Ejemplo:** `async with async_playwright() as playwright:`

### **List Comprehension**
Sintaxis concisa para crear listas basadas en iterables existentes.
- **Ejemplo:** `[line.strip() for line in lines if line]`

### **Type Hints**
Anotaciones que indican el tipo de datos esperado en variables y funciones.
- **Ejemplo:** `def procesar(url: str) -> Optional[str]:`

---

## Términos de Web Scraping

### **Web Scraping**
Técnica automatizada para extraer datos de páginas web, simulando la navegación humana.

### **Playwright**
Framework moderno para automatización web que puede controlar navegadores reales (Chrome, Firefox, Safari).
- **Ventajas:** Maneja JavaScript, es más rápido que Selenium
- **Uso:** Ideal para páginas con contenido dinámico

### **Headless Browser**
Navegador que funciona sin interfaz gráfica, solo por línea de comandos.
- **Beneficio:** Menor consumo de recursos, ideal para automatización

### **DOM (Document Object Model)**
Representación estructurada del contenido HTML de una página web.

### **Wait Strategies**
Técnicas para esperar que el contenido se cargue completamente:
- **`load`:** Espera que se cargue el HTML básico
- **`domcontentloaded`:** Espera que se construya el DOM
- **`networkidle`:** Espera que no haya actividad de red por un período

---

## Términos de Markdown

### **Markdown**
Lenguaje de marcado ligero que permite formatear texto usando sintaxis simple.
- **Ejemplo:** `# Título`, `**negrita**`, `*cursiva*`

### **MDX**
Extensión de Markdown que permite incluir componentes de React/JSX.
- **Uso:** Documentación interactiva, blogs técnicos

### **Markdownify**
Biblioteca de Python que convierte HTML a Markdown automáticamente.

---

## Términos de Archivos y Rutas

### **Ruta Absoluta vs Relativa**
- **Absoluta:** Ruta completa desde la raíz (`C:/Users/usuario/archivo.html`)
- **Relativa:** Ruta desde el directorio actual (`./archivo.html`)

### **File URI Scheme**
Protocolo para referenciar archivos locales en navegadores.
- **Formato:** `file:///C:/ruta/completa/archivo.html`
- **Uso:** Permite que Playwright acceda a archivos locales

### **Path (pathlib)**
Biblioteca moderna de Python para manipular rutas de archivos de forma multiplataforma.

---

## Términos de Logging y Debugging

### **Logging**
Sistema para registrar eventos y errores durante la ejecución del programa.
- **Niveles:** DEBUG, INFO, WARNING, ERROR, CRITICAL

### **Exception Handling**
Manejo de errores usando bloques `try`, `except`, `finally`.

### **Stack Trace**
Información detallada sobre dónde ocurrió un error en el código.

---

## Términos de Configuración

### **JSON (JavaScript Object Notation)**
Formato de intercambio de datos legible por humanos y máquinas.
- **Uso:** Archivos de configuración, APIs, almacenamiento de datos

### **Environment Variables**
Variables del sistema operativo que contienen configuración.
- **Ejemplo:** `OUTPUT_DIR=C:/salida python script.py`

### **Command Line Arguments**
Parámetros pasados al programa desde la terminal.
- **Ejemplo:** `python script.py --config archivo.json --verbose`

---

## Términos de Rendimiento

### **Concurrencia vs Paralelismo**
- **Concurrencia:** Múltiples tareas progresando al mismo tiempo (una CPU)
- **Paralelismo:** Múltiples tareas ejecutándose simultáneamente (múltiples CPUs)

### **Semáforo (Semaphore)**
Mecanismo para controlar el acceso concurrente a recursos limitados.
- **Ejemplo:** Limitar a máximo 3 conexiones simultáneas

### **Race Condition**
Error que ocurre cuando múltiples procesos acceden al mismo recurso sin coordinación.

### **Memory Leak**
Problema donde el programa no libera memoria que ya no usa, causando aumento progresivo del consumo.

---

## Términos de Arquitectura de Software

### **Separation of Concerns**
Principio de diseño que separa diferentes funcionalidades en módulos distintos.

### **DRY (Don't Repeat Yourself)**
Principio que evita la duplicación de código mediante reutilización y abstracción.

### **SOLID Principles**
Conjunto de principios para escribir código limpio y mantenible.

### **Refactoring**
Proceso de reestructurar código existente sin cambiar su funcionalidad externa.

---

## Términos de Testing y Calidad

### **Unit Testing**
Pruebas que verifican componentes individuales del código.

### **Integration Testing**
Pruebas que verifican la interacción entre diferentes módulos.

### **Edge Cases**
Situaciones extremas o poco comunes que podrían causar errores.

### **Code Coverage**
Métrica que indica qué porcentaje del código es ejecutado por las pruebas.

---

## Términos de Control de Versiones

### **Git**
Sistema de control de versiones distribuido para rastrear cambios en el código.

### **Repository (Repo)**
Directorio que contiene el proyecto y su historial de cambios.

### **Commit**
Snapshot o fotografía del estado del código en un momento específico.

### **Branch**
Línea de desarrollo paralela que permite trabajar en características sin afectar el código principal.

---

## Términos de Deployment y DevOps

### **Environment**
Configuración específica donde se ejecuta el código (desarrollo, pruebas, producción).

### **CI/CD (Continuous Integration/Continuous Deployment)**
Práctica de integrar y desplegar código automáticamente.

### **Docker**
Plataforma para empaquetar aplicaciones en contenedores portables.

### **Virtual Environment**
Entorno aislado de Python con sus propias dependencias.

---

## Términos de Seguridad Web

### **CORS (Cross-Origin Resource Sharing)**
Mecanismo que permite que una página web acceda a recursos de otro dominio.

### **Rate Limiting**
Técnica para limitar el número de requests por período de tiempo.

### **User Agent**
String que identifica el navegador y sistema operativo al servidor web.

### **Robots.txt**
Archivo que indica a los crawlers qué partes del sitio pueden o no pueden acceder.

---

## Términos de Base de Datos

### **CRUD (Create, Read, Update, Delete)**
Operaciones básicas que se pueden realizar sobre datos.

### **Schema**
Estructura que define la organización de los datos.

### **Migration**
Script que modifica la estructura de la base de datos.

---

## Términos de Networking

### **HTTP Status Codes**
Códigos numéricos que indican el resultado de una petición web.
- **200:** OK
- **404:** Not Found
- **500:** Internal Server Error

### **Timeout**
Límite de tiempo máximo para esperar una respuesta.

### **SSL/TLS**
Protocolos de seguridad para comunicaciones web encriptadas (HTTPS).

---

## Términos Específicos del Proyecto

### **Fragment Identifier**
Parte de la URL después del `#` que indica una sección específica de la página.
- **Ejemplo:** `archivo.html#introduccion`

### **Content Extraction**
Proceso de obtener información específica de documentos web.

### **Batch Processing**
Procesamiento de múltiples elementos en lotes o grupos.

### **File Pattern Matching**
Técnica para encontrar archivos usando patrones como wildcards (`*.html`).

---

Este glosario te ayudará a entender todos los términos técnicos utilizados en el análisis del código y en las recomendaciones de mejora. Si necesitas aclaración sobre algún término específico, no dudes en consultar documentación adicional o recursos de aprendizaje en línea.