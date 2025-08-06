#!/usr/bin/env python3
"""
HTML to Markdown Scraper - Versión Profesional Mejorada
======================================================

Extractor profesional de contenido HTML a Markdown usando Playwright.

Mejoras implementadas:
- Manejo robusto de errores con logging profesional
- Configuración flexible desde archivos JSON
- Optimización de recursos (reutilización de navegador)
- Validaciones de entrada completas
- Procesamiento paralelo opcional
- Métricas y estadísticas detalladas
- Interfaz de línea de comandos avanzada
- Nombres de archivo inteligentes

Autor: Versión mejorada del código original
Fecha: 2025
"""

import asyncio
import json
import logging
import os
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass, asdict

from playwright.async_api import async_playwright, Browser, BrowserContext
from markdownify import markdownify as md


@dataclass
class EstadisticasProcesamiento:
    """Clase para almacenar estadísticas del procesamiento."""
    inicio: float = 0
    fin: float = 0
    archivos_procesados: int = 0
    archivos_fallidos: int = 0
    total_palabras: int = 0
    total_caracteres: int = 0
    urls_procesadas: List[str] = None
    urls_fallidas: List[str] = None
    
    def __post_init__(self):
        if self.urls_procesadas is None:
            self.urls_procesadas = []
        if self.urls_fallidas is None:
            self.urls_fallidas = []
    
    @property
    def duracion(self) -> float:
        """Calcula la duración total del procesamiento."""
        return self.fin - self.inicio if self.fin > self.inicio else 0
    
    @property
    def total_archivos(self) -> int:
        """Retorna el total de archivos procesados."""
        return self.archivos_procesados + self.archivos_fallidos
    
    @property
    def tasa_exito(self) -> float:
        """Calcula la tasa de éxito en porcentaje."""
        if self.total_archivos == 0:
            return 0
        return (self.archivos_procesados / self.total_archivos) * 100
    
    def imprimir_resumen(self):
        """Imprime un resumen detallado de las estadísticas."""
        print("\n" + "="*60)
        print("📊 ESTADÍSTICAS FINALES DEL PROCESAMIENTO")
        print("="*60)
        print(f"📄 Total de archivos procesados: {self.total_archivos}")
        print(f"✅ Exitosos: {self.archivos_procesados}")
        print(f"❌ Fallidos: {self.archivos_fallidos}")
        print(f"📈 Tasa de éxito: {self.tasa_exito:.1f}%")
        print(f"📝 Total de palabras extraídas: {self.total_palabras:,}")
        print(f"📏 Total de caracteres: {self.total_caracteres:,}")
        print(f"⏱️ Tiempo total: {self.duracion:.2f} segundos")
        
        if self.archivos_procesados > 0:
            tiempo_promedio = self.duracion / self.archivos_procesados
            palabras_promedio = self.total_palabras // self.archivos_procesados
            print(f"⚡ Tiempo promedio por archivo: {tiempo_promedio:.2f}s")
            print(f"📊 Palabras promedio por archivo: {palabras_promedio:,}")
        
        if self.urls_fallidas:
            print(f"\n❌ URLs que fallaron:")
            for url in self.urls_fallidas:
                print(f"   • {url}")
        
        print("="*60)


class HTMLToMarkdownScraper:
    """
    Extractor profesional de contenido HTML a Markdown usando Playwright.
    
    Esta clase maneja la extracción de contenido de archivos HTML locales o URLs remotas,
    convierte el contenido a Markdown y guarda los archivos con configuración flexible.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Inicializa el scraper con configuración desde archivo.
        
        Args:
            config_path: Ruta al archivo de configuración JSON
        """
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        self.stats = EstadisticasProcesamiento()
        self.browser: Optional[Browser] = None
        
        self.logger.info("🚀 HTML to Markdown Scraper inicializado")
        self.logger.info(f"📁 Configuración cargada desde: {config_path}")
    
    def _load_config(self, config_path: str) -> Dict:
        """
        Carga la configuración desde archivo JSON o usa valores por defecto.
        
        Args:
            config_path: Ruta al archivo de configuración
            
        Returns:
            Diccionario con la configuración cargada
        """
        default_config = {
            "urls": [
                "file:///C:/Users/frlpi/OneDrive/Documentos/ADSO/Fase%201%20-%20Analisis/Actividad%20de%20proyecto%201/1.%20Caracterizaci%C3%B3n%20de%20procesos/index.html#/introduccion",
                "file:///C:/Users/frlpi/OneDrive/Documentos/ADSO/Fase%201%20-%20Analisis/Actividad%20de%20proyecto%201/1.%20Caracterizaci%C3%B3n%20de%20procesos/index.html#/curso/tema1",
                "file:///C:/Users/frlpi/OneDrive/Documentos/ADSO/Fase%201%20-%20Analisis/Actividad%20de%20proyecto%201/1.%20Caracterizaci%C3%B3n%20de%20procesos/index.html#/curso/tema2",
                "file:///C:/Users/frlpi/OneDrive/Documentos/ADSO/Fase%201%20-%20Analisis/Actividad%20de%20proyecto%201/1.%20Caracterizaci%C3%B3n%20de%20procesos/index.html#/curso/tema3",
                "file:///C:/Users/frlpi/OneDrive/Documentos/ADSO/Fase%201%20-%20Analisis/Actividad%20de%20proyecto%201/1.%20Caracterizaci%C3%B3n%20de%20procesos/index.html#/curso/tema4"
            ],
            "output_dir": "C:/Users/frlpi/OneDrive/Escritorio/scraper",
            "options": {
                "headless": True,
                "wait_until": "networkidle",
                "timeout": 30000,
                "parallel": False,
                "max_concurrent": 3,
                "delay_between_requests": 1000,
                "retry_attempts": 2
            },
            "markdown": {
                "strip_elements": ["script", "style", "nav", "footer", "aside", "header"],
                "file_extension": ".mdx",
                "naming_pattern": "contenido_{index}",
                "smart_naming": True,
                "clean_excessive_whitespace": True
            },
            "logging": {
                "level": "INFO",
                "console": True,
                "file": True,
                "log_dir": "logs"
            }
        }
        
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # Fusión profunda de configuraciones
                    self._deep_merge_config(default_config, user_config)
                    print(f"✅ Configuración cargada desde: {config_path}")
            except json.JSONDecodeError as e:
                print(f"⚠️ Error en formato JSON de {config_path}: {e}")
                print("Usando configuración por defecto.")
            except Exception as e:
                print(f"⚠️ Error cargando configuración: {e}")
                print("Usando configuración por defecto.")
        else:
            print(f"📄 Archivo de configuración no encontrado: {config_path}")
            print("Usando configuración por defecto.")
        
        return default_config
    
    def _deep_merge_config(self, default: Dict, user: Dict) -> None:
        """
        Fusiona recursivamente la configuración del usuario con la por defecto.
        
        Args:
            default: Configuración por defecto (se modifica in-place)
            user: Configuración del usuario
        """
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self._deep_merge_config(default[key], value)
            else:
                default[key] = value
    
    def _setup_logging(self) -> logging.Logger:
        """
        Configura el sistema de logging profesional.
        
        Returns:
            Logger configurado para el scraper
        """
        log_config = self.config.get('logging', {})
        
        # Crear directorio de logs
        log_dir = Path(log_config.get('log_dir', 'logs'))
        log_dir.mkdir(exist_ok=True)
        
        # Configurar nivel de logging
        log_level = getattr(logging, log_config.get('level', 'INFO').upper())
        
        # Configurar handlers
        handlers = []
        
        if log_config.get('console', True):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            )
            handlers.append(console_handler)
        
        if log_config.get('file', True):
            log_filename = f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            log_path = log_dir / log_filename
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
            )
            handlers.append(file_handler)
        
        # Configurar logger
        logger = logging.getLogger('HTMLScraper')
        logger.setLevel(log_level)
        
        # Remover handlers existentes para evitar duplicados
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        for handler in handlers:
            logger.addHandler(handler)
        
        return logger
    
    def _validate_config(self) -> bool:
        """
        Valida la configuración antes de procesar.
        
        Returns:
            True si la configuración es válida, False en caso contrario
        """
        errores = []
        
        # Validar URLs
        if not self.config.get('urls'):
            errores.append("No se han especificado URLs para procesar")
        elif not isinstance(self.config['urls'], list):
            errores.append("Las URLs deben estar en formato de lista")
        
        # Validar directorio de salida
        if not self.config.get('output_dir'):
            errores.append("No se ha especificado directorio de salida")
        
        # Validar URLs de archivos locales
        urls_invalidas = []
        for url in self.config.get('urls', []):
            if url.startswith('file://'):
                # Limpiar la URL para obtener la ruta del archivo
                file_path = url.replace('file:///', '').split('#')[0]
                # Decodificar caracteres especiales en la URL
                file_path = file_path.replace('%20', ' ').replace('%C3%B3', 'ó')
                
                if not Path(file_path).exists():
                    urls_invalidas.append(f"Archivo no encontrado: {file_path}")
        
        if urls_invalidas:
            errores.extend(urls_invalidas)
        
        # Validar permisos de escritura
        try:
            output_path = Path(self.config['output_dir'])
            output_path.mkdir(parents=True, exist_ok=True)
            test_file = output_path / ".test_write_permission"
            test_file.write_text("test")
            test_file.unlink()
        except Exception as e:
            errores.append(f"Sin permisos de escritura en: {self.config['output_dir']} ({e})")
        
        # Mostrar errores si los hay
        if errores:
            self.logger.error("❌ Errores de configuración encontrados:")
            for error in errores:
                self.logger.error(f"   • {error}")
            return False
        
        self.logger.info("✅ Configuración validada correctamente")
        return True
    
    def _validate_urls(self) -> List[str]:
        """
        Valida y filtra las URLs que sean accesibles.
        
        Returns:
            Lista de URLs válidas
        """
        valid_urls = []
        
        for url in self.config['urls']:
            try:
                if url.startswith('file://'):
                    # Para archivos locales, verificar que existan
                    file_path = url.replace('file:///', '').split('#')[0]
                    file_path = file_path.replace('%20', ' ').replace('%C3%B3', 'ó')
                    
                    if Path(file_path).exists():
                        valid_urls.append(url)
                        self.logger.debug(f"✅ URL válida: {url}")
                    else:
                        self.logger.warning(f"⚠️ Archivo no encontrado: {file_path}")
                else:
                    # Para URLs remotas, asumir válidas (se verificarán al acceder)
                    valid_urls.append(url)
                    self.logger.debug(f"✅ URL remota: {url}")
            except Exception as e:
                self.logger.error(f"❌ Error validando URL {url}: {e}")
        
        self.logger.info(f"📊 URLs válidas encontradas: {len(valid_urls)}/{len(self.config['urls'])}")
        return valid_urls
    
    async def _init_browser(self) -> None:
        """Inicializa el navegador una sola vez para reutilización."""
        if self.browser is None:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=self.config['options']['headless']
            )
            self.logger.info("🌐 Navegador inicializado")
    
    async def _close_browser(self) -> None:
        """Cierra el navegador y limpia recursos."""
        if self.browser:
            await self.browser.close()
            await self.playwright.stop()
            self.browser = None
            self.logger.info("🔒 Navegador cerrado")
    
    async def _extract_content_safe(self, url: str, retry_count: int = 0) -> Optional[str]:
        """
        Extrae contenido HTML de forma segura con manejo de errores y reintentos.
        
        Args:
            url: URL a procesar
            retry_count: Número de intento actual
            
        Returns:
            Contenido HTML extraído o None si falla
        """
        context = None
        page = None
        max_retries = self.config['options'].get('retry_attempts', 2)
        
        try:
            await self._init_browser()
            
            context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            page = await context.new_page()
            
            self.logger.info(f"🌐 Accediendo a: {url}")
            
            # Configurar timeouts
            timeout = self.config['options'].get('timeout', 30000)
            wait_until = self.config['options'].get('wait_until', 'networkidle')
            
            await page.goto(url, wait_until=wait_until, timeout=timeout)
            
            # Esperar un poco más para contenido dinámico
            await page.wait_for_timeout(2000)
            
            content = await page.content()
            
            if content and len(content) > 100:  # Verificar que el contenido no esté vacío
                self.logger.info(f"✅ Contenido extraído: {len(content):,} caracteres")
                return content
            else:
                self.logger.warning(f"⚠️ Contenido sospechosamente corto: {len(content) if content else 0} caracteres")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Error extrayendo contenido de {url}: {type(e).__name__}: {e}")
            
            # Reintentar si no se ha alcanzado el máximo
            if retry_count < max_retries:
                self.logger.info(f"🔄 Reintentando ({retry_count + 1}/{max_retries})...")
                await asyncio.sleep(2)  # Esperar antes de reintentar
                return await self._extract_content_safe(url, retry_count + 1)
            
            return None
            
        finally:
            if page:
                await page.close()
            if context:
                await context.close()
    
    def _generate_smart_filename(self, url: str, index: int) -> str:
        """
        Genera nombres de archivo inteligentes basados en el contenido de la URL.
        
        Args:
            url: URL a procesar
            index: Índice secuencial
            
        Returns:
            Nombre de archivo generado
        """
        pattern = self.config['markdown']['naming_pattern']
        extension = self.config['markdown']['file_extension']
        smart_naming = self.config['markdown'].get('smart_naming', True)
        
        if smart_naming and '#' in url:
            # Extraer el fragmento de la URL
            fragment = url.split('#')[-1]
            # Limpiar caracteres especiales
            fragment = fragment.replace('/', '_').replace('\\', '_')
            fragment = ''.join(c for c in fragment if c.isalnum() or c in '_-')
            filename = f"{fragment}_{index:02d}"
        else:
            filename = pattern.format(index=index)
        
        return f"{filename}{extension}"
    
    def _convert_to_markdown(self, html_content: str) -> str:
        """
        Convierte HTML a Markdown con opciones configurables.
        
        Args:
            html_content: Contenido HTML a convertir
            
        Returns:
            Contenido convertido a Markdown
        """
        if not html_content:
            return ""
        
        try:
            markdown_config = self.config['markdown']
            
            markdown_content = md(
                html_content,
                strip=markdown_config.get('strip_elements', ['script', 'style']),
                convert=['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 
                        'a', 'strong', 'em', 'code', 'pre', 'blockquote', 
                        'table', 'tr', 'td', 'th', 'img'],
                heading_style='ATX'
            )
            
            # Limpiar contenido si está habilitado
            if markdown_config.get('clean_excessive_whitespace', True):
                markdown_content = self._clean_markdown(markdown_content)
            
            return markdown_content
            
        except Exception as e:
            self.logger.error(f"❌ Error convirtiendo a Markdown: {e}")
            return ""
    
    def _clean_markdown(self, markdown: str) -> str:
        """
        Limpia y optimiza el contenido Markdown.
        
        Args:
            markdown: Contenido Markdown a limpiar
            
        Returns:
            Contenido Markdown limpio
        """
        if not markdown:
            return ""
        
        # Separar en líneas
        lines = markdown.split('\n')
        cleaned_lines = []
        empty_count = 0
        
        for line in lines:
            line = line.rstrip()  # Quitar espacios al final
            
            if line.strip():
                cleaned_lines.append(line)
                empty_count = 0
            else:
                empty_count += 1
                # Máximo 2 líneas vacías consecutivas
                if empty_count <= 2:
                    cleaned_lines.append('')
        
        # Unir líneas y limpiar el inicio y final
        result = '\n'.join(cleaned_lines).strip()
        
        # Reemplazar múltiples espacios por uno solo
        import re
        result = re.sub(r' +', ' ', result)
        
        return result
    
    def _save_markdown_file(self, content: str, filename: str) -> bool:
        """
        Guarda contenido Markdown en archivo.
        
        Args:
            content: Contenido a guardar
            filename: Nombre del archivo
            
        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        if not content or not content.strip():
            self.logger.warning(f"⚠️ Contenido vacío para {filename}")
            return False
        
        try:
            output_path = Path(self.config['output_dir']) / filename
            
            # Verificar si archivo existe
            if output_path.exists():
                self.logger.info(f"📝 Sobrescribiendo archivo existente: {filename}")
            
            # Guardar archivo
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Calcular métricas
            word_count = len(content.split())
            char_count = len(content)
            
            # Actualizar estadísticas
            self.stats.total_palabras += word_count
            self.stats.total_caracteres += char_count
            
            self.logger.info(f"✅ Archivo guardado: {filename} ({word_count:,} palabras, {char_count:,} caracteres)")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error guardando archivo {filename}: {e}")
            return False
    
    async def _process_single_url(self, url: str, index: int) -> bool:
        """
        Procesa una URL individual completamente.
        
        Args:
            url: URL a procesar
            index: Índice secuencial
            
        Returns:
            True si se procesó exitosamente, False en caso contrario
        """
        try:
            self.logger.info(f"📄 Procesando [{index}]: {url}")
            
            # Extraer contenido HTML
            html_content = await self._extract_content_safe(url)
            if not html_content:
                self.stats.archivos_fallidos += 1
                self.stats.urls_fallidas.append(url)
                return False
            
            # Convertir a Markdown
            markdown_content = self._convert_to_markdown(html_content)
            if not markdown_content:
                self.logger.error(f"❌ Fallo en conversión a Markdown para: {url}")
                self.stats.archivos_fallidos += 1
                self.stats.urls_fallidas.append(url)
                return False
            
            # Generar nombre de archivo y guardar
            filename = self._generate_smart_filename(url, index)
            success = self._save_markdown_file(markdown_content, filename)
            
            if success:
                self.stats.archivos_procesados += 1
                self.stats.urls_procesadas.append(url)
                return True
            else:
                self.stats.archivos_fallidos += 1
                self.stats.urls_fallidas.append(url)
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error procesando {url}: {e}")
            self.stats.archivos_fallidos += 1
            self.stats.urls_fallidas.append(url)
            return False
    
    async def run_sequential(self) -> None:
        """Ejecuta procesamiento secuencial (recomendado para archivos locales)."""
        self.logger.info("🚀 Iniciando procesamiento secuencial")
        
        # Validar configuración
        if not self._validate_config():
            self.logger.error("❌ Configuración inválida. Abortando procesamiento.")
            return
        
        # Obtener URLs válidas
        valid_urls = self._validate_urls()
        if not valid_urls:
            self.logger.error("❌ No hay URLs válidas para procesar")
            return
        
        self.logger.info(f"📊 Iniciando procesamiento de {len(valid_urls)} URLs")
        self.stats.inicio = time.time()
        
        try:
            for i, url in enumerate(valid_urls, 1):
                await self._process_single_url(url, i)
                
                # Pausa entre requests si está configurada
                delay = self.config['options'].get('delay_between_requests', 1000)
                if delay > 0 and i < len(valid_urls):  # No pausar después del último
                    await asyncio.sleep(delay / 1000.0)  # Convertir ms a segundos
                    
        except KeyboardInterrupt:
            self.logger.warning("⏹️ Procesamiento interrumpido por el usuario")
        except Exception as e:
            self.logger.error(f"❌ Error fatal durante procesamiento: {e}")
        finally:
            await self._close_browser()
            self.stats.fin = time.time()
            self._print_final_stats()
    
    async def run_parallel(self, max_concurrent: Optional[int] = None) -> None:
        """
        Ejecuta procesamiento paralelo (recomendado para URLs remotas).
        
        Args:
            max_concurrent: Número máximo de tareas concurrentes
        """
        self.logger.info("🚀 Iniciando procesamiento paralelo")
        
        # Validar configuración
        if not self._validate_config():
            self.logger.error("❌ Configuración inválida. Abortando procesamiento.")
            return
        
        # Obtener URLs válidas
        valid_urls = self._validate_urls()
        if not valid_urls:
            self.logger.error("❌ No hay URLs válidas para procesar")
            return
        
        # Configurar concurrencia
        if max_concurrent is None:
            max_concurrent = self.config['options'].get('max_concurrent', 3)
        
        self.logger.info(f"📊 Iniciando procesamiento paralelo de {len(valid_urls)} URLs (max {max_concurrent} concurrentes)")
        self.stats.inicio = time.time()
        
        # Semáforo para controlar concurrencia
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(url: str, index: int) -> bool:
            async with semaphore:
                return await self._process_single_url(url, index)
        
        try:
            # Crear tareas para todas las URLs
            tasks = [
                process_with_semaphore(url, i) 
                for i, url in enumerate(valid_urls, 1)
            ]
            
            # Ejecutar todas las tareas
            await asyncio.gather(*tasks, return_exceptions=True)
                
        except KeyboardInterrupt:
            self.logger.warning("⏹️ Procesamiento interrumpido por el usuario")
        except Exception as e:
            self.logger.error(f"❌ Error fatal durante procesamiento paralelo: {e}")
        finally:
            await self._close_browser()
            self.stats.fin = time.time()
            self._print_final_stats()
    
    def _print_final_stats(self) -> None:
        """Imprime estadísticas finales del procesamiento."""
        self.stats.imprimir_resumen()
        self.logger.info("🏁 Procesamiento completado")
        
        # Guardar estadísticas en archivo JSON
        try:
            stats_file = Path(self.config['output_dir']) / "estadisticas_procesamiento.json"
            with open(stats_file, 'w', encoding='utf-8') as f:
                # Convertir dataclass a dict, excluyendo campos que no son serializables
                stats_dict = asdict(self.stats)
                stats_dict['fecha_procesamiento'] = datetime.now().isoformat()
                stats_dict['configuracion_utilizada'] = self.config
                json.dump(stats_dict, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📊 Estadísticas guardadas en: {stats_file}")
        except Exception as e:
            self.logger.error(f"❌ Error guardando estadísticas: {e}")


def create_sample_config(config_path: str = "config_ejemplo.json") -> None:
    """
    Crea un archivo de configuración de ejemplo.
    
    Args:
        config_path: Ruta donde crear el archivo de configuración
    """
    sample_config = {
        "urls": [
            "file:///C:/ruta/a/tu/archivo1.html",
            "file:///C:/ruta/a/tu/archivo2.html",
            "https://ejemplo.com/pagina1",
            "https://ejemplo.com/pagina2"
        ],
        "output_dir": "salida_markdown",
        "options": {
            "headless": True,
            "wait_until": "networkidle",
            "timeout": 30000,
            "parallel": False,
            "max_concurrent": 3,
            "delay_between_requests": 1000,
            "retry_attempts": 2
        },
        "markdown": {
            "strip_elements": ["script", "style", "nav", "footer", "aside", "header"],
            "file_extension": ".md",
            "naming_pattern": "contenido_{index}",
            "smart_naming": True,
            "clean_excessive_whitespace": True
        },
        "logging": {
            "level": "INFO",
            "console": True,
            "file": True,
            "log_dir": "logs"
        }
    }
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(sample_config, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Archivo de configuración de ejemplo creado: {config_path}")
        print("✏️ Edita este archivo para personalizar tu configuración.")
        
    except Exception as e:
        print(f"❌ Error creando archivo de configuración: {e}")


def parse_arguments() -> argparse.Namespace:
    """
    Analiza los argumentos de línea de comandos.
    
    Returns:
        Argumentos analizados
    """
    parser = argparse.ArgumentParser(
        description='HTML to Markdown Scraper Profesional',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s --create-config
  %(prog)s --config mi_config.json
  %(prog)s --config config.json --parallel
  %(prog)s --urls "file:///archivo1.html" "file:///archivo2.html" --output "salida"
        """
    )
    
    parser.add_argument(
        '--config', 
        default='config.json',
        help='Archivo de configuración JSON (default: config.json)'
    )
    
    parser.add_argument(
        '--create-config', 
        action='store_true',
        help='Crear archivo de configuración de ejemplo'
    )
    
    parser.add_argument(
        '--parallel', 
        action='store_true',
        help='Usar procesamiento paralelo'
    )
    
    parser.add_argument(
        '--urls', 
        nargs='+',
        help='Lista de URLs a procesar (sobrescribe configuración)'
    )
    
    parser.add_argument(
        '--output', 
        help='Directorio de salida (sobrescribe configuración)'
    )
    
    parser.add_argument(
        '--headless', 
        action='store_true',
        help='Ejecutar navegador en modo headless'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Activar logging detallado (DEBUG)'
    )
    
    return parser.parse_args()


async def main() -> None:
    """Función principal mejorada con manejo completo de argumentos."""
    args = parse_arguments()
    
    # Crear configuración de ejemplo si se solicita
    if args.create_config:
        create_sample_config()
        return
    
    try:
        # Inicializar scraper
        scraper = HTMLToMarkdownScraper(args.config)
        
        # Sobrescribir configuración con argumentos de línea de comandos
        if args.urls:
            scraper.config['urls'] = args.urls
            scraper.logger.info(f"📝 URLs sobrescritas desde línea de comandos: {len(args.urls)} URLs")
        
        if args.output:
            scraper.config['output_dir'] = args.output
            scraper.logger.info(f"📁 Directorio de salida sobrescrito: {args.output}")
        
        if args.headless:
            scraper.config['options']['headless'] = True
        
        if args.verbose:
            scraper.config['logging']['level'] = 'DEBUG'
            scraper.logger.setLevel(logging.DEBUG)
            scraper.logger.debug("🔍 Modo verbose activado")
        
        # Ejecutar procesamiento
        if args.parallel or scraper.config['options'].get('parallel', False):
            await scraper.run_parallel()
        else:
            await scraper.run_sequential()
            
    except KeyboardInterrupt:
        print("\n⏹️ Procesamiento interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        logging.error(f"Error fatal: {e}", exc_info=True)


if __name__ == "__main__":
    # Verificar dependencias
    try:
        import playwright
        import markdownify
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("📦 Instala las dependencias con:")
        print("   pip install playwright markdownify")
        print("   playwright install")
        exit(1)
    
    # Ejecutar programa principal
    asyncio.run(main())