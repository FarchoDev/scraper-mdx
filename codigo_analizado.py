import asyncio
from playwright.async_api import async_playwright
from markdownify import markdownify as md
import os

# === CONFIGURACIÓN ===
URLS = [
    "file:///C:/Users/frlpi/OneDrive/Documentos/ADSO/Fase%201%20-%20Analisis/Actividad%20de%20proyecto%201/1.%20Caracterizaci%C3%B3n%20de%20procesos/index.html#/introduccion",
    "file:///C:/Users/frlpi/OneDrive/Documentos/ADSO/Fase%201%20-%20Analisis/Actividad%20de%20proyecto%201/1.%20Caracterizaci%C3%B3n%20de%20procesos/index.html#/curso/tema1",
    "file:///C:/Users/frlpi/OneDrive/Documentos/ADSO/Fase%201%20-%20Analisis/Actividad%20de%20proyecto%201/1.%20Caracterizaci%C3%B3n%20de%20procesos/index.html#/curso/tema2",
    "file:///C:/Users/frlpi/OneDrive/Documentos/ADSO/Fase%201%20-%20Analisis/Actividad%20de%20proyecto%201/1.%20Caracterizaci%C3%B3n%20de%20procesos/index.html#/curso/tema3",
    "file:///C:/Users/frlpi/OneDrive/Documentos/ADSO/Fase%201%20-%20Analisis/Actividad%20de%20proyecto%201/1.%20Caracterizaci%C3%B3n%20de%20procesos/index.html#/curso/tema4",
]
OUTPUT_DIR = "C:/Users/frlpi/OneDrive/Escritorio/scraper"

# === FUNCIONES ===

async def extraer_contenido(playwright, ruta_local):
    browser = await playwright.chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()

    await page.goto(ruta_local, wait_until="networkidle")
    content = await page.content()

    await browser.close()
    return content

def convertir_y_guardar_html_a_markdown(html_content, nombre_archivo):
    markdown = md(html_content, strip=['script', 'style'])
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ruta_archivo = os.path.join(OUTPUT_DIR, nombre_archivo)
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"✅ Archivo guardado en: {ruta_archivo}")

# === FLUJO PRINCIPAL ===
async def main():
    async with async_playwright() as playwright:
        for i, ruta_local in enumerate(URLS, start=1):
            print(f"Procesando archivo {i} / {len(URLS)}: {ruta_local}")
            html = await extraer_contenido(playwright, ruta_local)
            nombre_archivo = f"contenido_{i}.mdx"
            convertir_y_guardar_html_a_markdown(html, nombre_archivo)

if __name__ == "__main__":
    asyncio.run(main())