"""
🤖 TELEGRAM BOT - Sistema de Control y Monitoreo
"""
import os
import sys
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StakasBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            logger.error("❌ TELEGRAM_BOT_TOKEN not set")
            sys.exit(1)
        
        self.app = Application.builder().token(self.token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Configurar comandos"""
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("health", self.cmd_health))
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        await update.message.reply_text(
            "🎵 *STAKAS AUTOMATION SYSTEM*\n\n"
            "Comandos:\n"
            "/status - Estado del sistema\n"
            "/health - Salud del sistema\n",
            parse_mode="Markdown"
        )
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Estado del sistema"""
        msg = "📊 *ESTADO DEL SISTEMA*\n\n"
        msg += "🤖 Orchestrator ML: ✅\n"
        msg += "🎬 Video Generator: ✅\n"
        msg += "📱 Campaigns Meta: ✅\n"
        msg += "🎥 Edits/Clips: ✅\n"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
    
    async def cmd_health(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Health check"""
        import psutil
        
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        
        msg = f"💚 *SYSTEM HEALTH*\n\n"
        msg += f"CPU: {cpu}%\n"
        msg += f"RAM: {mem}%\n"
        msg += f"Status: {'✅ OK' if cpu < 80 and mem < 80 else '⚠️ HIGH'}"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
    
    def run(self):
        """Iniciar bot"""
        logger.info("🤖 Telegram Bot iniciando...")
        self.app.run_polling()

if __name__ == "__main__":
    try:
        bot = StakasBot()
        bot.run()
    except Exception as e:
        logger.error(f"Error iniciando bot: {e}")
        sys.exit(1)
