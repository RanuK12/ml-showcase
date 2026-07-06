#!/usr/bin/env python3
"""
Herramienta de Automatización de Informes Financieros con API de Fincept
Autor: Ranukita
Versión: 1.0.0
Fecha: 2026-07-06

Esta herramienta permite generar informes financieros personalizados utilizando
datos de la API de Fincept (https://api.fincept.in/).
"""

import os
import sys
import yaml
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('financial_report_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Agregar ruta de módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.fincept_api import FinceptAPI
from utils.report_generator import ReportGenerator

def load_config(config_path: str = "config.yaml") -> Dict:
    """Cargar configuración desde archivo YAML.
    
    Args:
        config_path: Ruta al archivo de configuración YAML
        
    Returns:
        Diccionario con la configuración cargada
    """
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        logger.info(f"Configuración cargada desde {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Archivo de configuración no encontrado: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error al parsear YAML: {e}")
        raise

def validate_config(config: Dict) -> bool:
    """Validar la estructura de la configuración.
    
    Args:
        config: Diccionario con la configuración
        
    Returns:
        True si la configuración es válida, False en caso contrario
    """
    if not config or 'reports' not in config:
        logger.error("Estructura de configuración inválida: falta 'reports'")
        return False
    
    required_keys = ['name', 'type', 'period', 'output']
    for report in config['reports']:
        for key in required_keys:
            if key not in report:
                logger.error(f"Falta clave requerida en reporte '{report.get('name', 'desconocido')}': {key}")
                return False
        
        if 'format' not in report['output'] or 'path' not in report['output']:
            logger.error(f"Configuración de salida inválida en reporte '{report['name']}'")
            return False
    
    return True

def generate_reports(config: Dict, fincept_api: FinceptAPI, report_generator: ReportGenerator) -> List[str]:
    """Generar todos los informes configurados.
    
    Args:
        config: Diccionario con la configuración
        fincept_api: Instancia de FinceptAPI
        report_generator: Instancia de ReportGenerator
        
    Returns:
        Lista de rutas a los informes generados
    """
    generated_files = []
    
    for report_config in config.get('reports', []):
        report_name = report_config['name']
        report_type = report_config['type']
        period = report_config['period']
        filters = report_config.get('filters', {})
        output_format = report_config['output']['format']
        output_path = report_config['output']['path']
        
        logger.info(f"Generando informe: {report_name} ({report_type})")
        
        try:
            # Obtener datos de Fincept API
            if report_type == "balance_sheet":
                data = fincept_api.get_balance_sheet(period=period, filters=filters)
            elif report_type == "income_statement":
                data = fincept_api.get_income_statement(period=period, filters=filters)
            elif report_type == "cash_flow":
                data = fincept_api.get_cash_flow(period=period, filters=filters)
            elif report_type == "financial_analysis":
                data = fincept_api.get_financial_analysis(period=period, filters=filters)
            elif report_type == "valuation":
                data = fincept_api.get_valuation(period=period, filters=filters)
            else:
                logger.warning(f"Tipo de informe no soportado: {report_type}")
                continue
            
            # Generar informe en el formato especificado
            if output_format == "excel":
                filename = report_generator.generate_excel_report(data, report_name)
            elif output_format == "csv":
                filename = report_generator.generate_csv_report(data, report_name)
            elif output_format == "json":
                filename = report_generator.generate_json_report(data, report_name)
            elif output_format == "pdf":
                filename = report_generator.generate_pdf_report(data, report_name)
            else:
                logger.error(f"Formato de salida no soportado: {output_format}")
                continue
            
            logger.info(f"✅ Informe generado: {filename}")
            generated_files.append(filename)
            
        except Exception as e:
            logger.error(f"❌ Error generando informe {report_name}: {e}")
            continue
    
    return generated_files

def main():
    """Punto de entrada principal de la aplicación."""
    logger.info("Iniciando herramienta de automatización de informes financieros con Fincept API")
    
    try:
        # Cargar configuración
        config = load_config()
        
        # Validar configuración
        if not validate_config(config):
            logger.error("Configuración inválida. Revise el archivo config.yaml")
            sys.exit(1)
        
        # Inicializar API y generador de informes
        fincept_api = FinceptAPI()
        report_generator = ReportGenerator()
        
        # Generar informes
        generated_files = generate_reports(config, fincept_api, report_generator)
        
        # Resumen final
        logger.info(f"\n{'='*60}")
        logger.info("RESUMEN DE GENERACIÓN DE INFORMES")
        logger.info(f"{'='*60}")
        logger.info(f"Total de informes generados: {len(generated_files)}")
        for file in generated_files:
            logger.info(f"  ✓ {file}")
        
        if generated_files:
            logger.info(f"\n🎉 Todos los informes se generaron correctamente!")
            logger.info(f"📁 Ruta de salida: {os.path.abspath('output')}")
        else:
            logger.warning("⚠️ No se generó ningún informe")
            
    except Exception as e:
        logger.critical(f"❌ Error crítico: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()