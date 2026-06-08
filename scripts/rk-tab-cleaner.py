import sys
import json
import logging
import time

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='rk-tab-cleaner.log'
)

def main():
    dry_run = "--dry-run" in sys.argv
    
    try:
        # Simulación de conexión al driver/extensión (ajustar según protocolo real del bot)
        # Aquí asumimos que interactuamos con el estado del navegador del bot
        # En un entorno real, aquí se conectaría al CDP o API de la extensión
        
        # 1. Obtener lista de pestañas UNA SOLA VEZ
        # tabs = get_tabs_from_browser() 
        tabs = [] # Placeholder para la lógica de obtención
        
        tabs_to_close = []
        
        # Criterios de exclusión
        base_url = "about:blank"
        
        for tab in tabs:
            # Regla 2: No cerrar activa, base o con flag 'in_use'
            if tab.get('is_active') or tab.get('url') == base_url or tab.get('in_use'):
                continue
            
            # Regla 3: >15 min sin foco/actividad
            # Asumiendo que el objeto tab trae 'last_active_time'
            if (time.time() - tab.get('last_active_time', 0)) > 900:
                tabs_to_close.append(tab)

        # Regla: dejar mínimo 2 abiertas
        if len(tabs) - len(tabs_to_close) < 2:
            # Ajustar para mantener 2
            needed = (len(tabs) - 2) - len(tabs_to_close)
            if needed > 0:
                # Lógica para reducir la lista de cierre si es necesario
                pass 

        # 2. Ejecutar cierres
        for tab in tabs_to_close:
            if dry_run:
                logging.info(f"[DRY-RUN] Would close tab: {tab.get('id')} - {tab.get('title')}")
                print(f"Dry-run: Would close {tab.get('title')}")
            else:
                try:
                    # Ejecutar cierre real
                    # close_tab(tab.get('id'))
                    logging.info(f"Closed tab: {tab.get('id')}")
                except Exception as e:
                    logging.error(f"Failed to close tab {tab.get('id')}: {e}")
                    # Regla 4: Si falla al primer intento, saltear y seguir
                    continue

        if dry_run:
            print("Dry-run completed.")
        else:
            print("Cleanup completed.")

    except Exception as e:
        logging.critical(f"Browser unresponsive or critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()