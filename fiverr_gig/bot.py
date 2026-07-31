#!/usr/bin/env python3
"""
Bot de Trading / Copy-Trading Cripto a Medida en Python
Desarrollado por Ranuk IT Solutions
"""

import asyncio
import logging
import os
import argparse
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self, mode='live'):
        self.mode = mode
        self.strategies = {}
        self.risk_manager = None
        self.telegram_notifier = None
        self.dashboard = None
        
    async def initialize(self):
        """Inicializar componentes del bot"""
        logger.info("Inicializando bot de trading en modo: %s", self.mode)
        
        # Inicializar gestor de riesgo
        from risk_manager import RiskManager
        self.risk_manager = RiskManager()
        
        # Inicializar notificador de Telegram
        from telegram_notifier import TelegramNotifier
        self.telegram_notifier = TelegramNotifier()
        
        # Inicializar dashboard
        from dashboard import Dashboard
        self.dashboard = Dashboard()
        
        # Cargar estrategias
        await self.load_strategies()
        
    async def load_strategies(self):
        """Cargar estrategias disponibles"""
        from strategies.grid_trading import GridTrading
        from strategies.momentum_sniper import MomentumSniper
        from strategies.copy_trading import CopyTrading
        from strategies.arbitrage import Arbitrage
        from strategies.market_making import MarketMaking
        
        self.strategies = {
            'grid': GridTrading(),
            'momentum': MomentumSniper(),
            'copy': CopyTrading(),
            'arbitrage': Arbitrage(),
            'market_making': MarketMaking()
        }
        
        logger.info("Estrategias cargadas: %s", list(self.strategies.keys()))
    
    async def run(self):
        """Ejecutar el bot principal"""
        await self.initialize()
        
        logger.info("Iniciando bot de trading...")
        
        if self.mode == 'paper':
            await self.run_paper_trading()
        else:
            await self.run_live_trading()
    
    async def run_paper_trading(self):
        """Ejecutar en modo paper trading (simulación)"""
        logger.info("Ejecutando en modo paper trading")
        
        # Simular trading sin capital real
        while True:
            for name, strategy in self.strategies.items():
                try:
                    await strategy.execute_paper_trade()
                    logger.info("Ejecutada estrategia paper: %s", name)
                except Exception as e:
                    logger.error("Error en estrategia %s: %s", name, str(e))
            
            await asyncio.sleep(60)  # Esperar 1 minuto entre ejecuciones
    
    async def run_live_trading(self):
        """Ejecutar en modo trading real"""
        logger.info("Ejecutando en modo trading real")
        
        while True:
            # Verificar salud de APIs
            await self.check_apis_health()
            
            # Ejecutar estrategias
            for name, strategy in self.strategies.items():
                try:
                    # Verificar risk management
                    if await self.risk_manager.can_execute_strategy(name):
                        await strategy.execute_trade()
                        logger.info("Ejecutada estrategia: %s", name)
                except Exception as e:
                    logger.error("Error en estrategia %s: %s", name, str(e))
            
            await asyncio.sleep(30)  # Esperar 30 segundos entre ejecuciones
    
    async def check_apis_health(self):
        """Verificar salud de APIs de exchanges"""
        # Implementar verificación de APIs
        pass
    
    def stop(self):
        """Detener el bot"""
        logger.info("Deteniendo bot de trading...")
        # Implementar lógica de detención segura

async def main():
    parser = argparse.ArgumentParser(description='Bot de Trading Cripto')
    parser.add_argument('--mode', choices=['live', 'paper'], default='live',
                       help='Modo de ejecución (live o paper)')
    args = parser.parse_args()
    
    bot = TradingBot(mode=args.mode)
    try:
        await bot.run()
    except KeyboardInterrupt:
        bot.stop()
        logger.info("Bot detenido por usuario")

if __name__ == "__main__":
    asyncio.run(main())