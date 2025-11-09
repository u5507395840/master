"""
Telegram Bot - Control remoto del sistema
"""
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_BASE = os.getenv("API_BASE", "http://localhost:8080")

class StakazoBotHandler:
    def __init__(self):
        self.api_base = API_BASE
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome = """
🎵 **Bienvenido al Bot de Stakazo**

Comandos disponibles:

📊 `/status` - Estado del sistema
🚀 `/launch <artista> <track>` - Lanzar campaña
📈 `/metrics` - Ver métricas
💡 `/strategy <artista> <track>` - Generar estrategia IA
🎬 `/video <artista> <track>` - Generar descripción viral

Ejemplo:
`/launch Bad Bunny "Un Preview"`
        """
        await update.message.reply_text(welcome, parse_mode='Markdown')
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        try:
            response = requests.get(f"{self.api_base}/health", timeout=5)
            data = response.json()
            
            status_msg = f"""
📊 **Estado del Sistema**

🟢 Status: {data.get('status', 'unknown').upper()}
🖥️  CPU: {data.get('cpu_percent', 0):.1f}%
💾 RAM: {data.get('memory_percent', 0):.1f}%
🤖 OpenAI: {'✅' if data.get('openai_configured') else '❌'}
⚙️  Modo: {data.get('mode', 'unknown').upper()}
            """
            
            await update.message.reply_text(status_msg, parse_mode='Markdown')
        
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def launch_campaign(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /launch"""
        if len(context.args) < 2:
            await update.message.reply_text("Uso: /launch <artista> <track>")
            return
        
        artist = context.args[0]
        track = " ".join(context.args[1:])
        
        await update.message.reply_text(f"🚀 Lanzando campaña para {artist} - {track}...")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/campaign/launch",
                json={
                    "artist": artist,
                    "track": track,
                    "platforms": ["TikTok", "Instagram", "YouTube"]
                },
                timeout=10
            )
            
            data = response.json()
            
            result_msg = f"""
✅ **Campaña Lanzada**

🎤 Artista: {data.get('artist')}
🎵 Track: {data.get('track')}
🆔 Campaign ID: {data.get('campaign_id')}
📱 Plataformas: {', '.join(data.get('platforms', []))}

🎬 Video generado: {'✅' if data.get('video_generated') else '⏳ Pendiente'}

Usa /metrics para ver el progreso.
            """
            
            await update.message.reply_text(result_msg, parse_mode='Markdown')
        
        except Exception as e:
            await update.message.reply_text(f"❌ Error al lanzar campaña: {str(e)}")
    
    async def generate_strategy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /strategy"""
        if len(context.args) < 2:
            await update.message.reply_text("Uso: /strategy <artista> <track>")
            return
        
        artist = context.args[0]
        track = " ".join(context.args[1:])
        
        await update.message.reply_text(f"🧠 Generando estrategia con IA para {artist} - {track}...")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/openai/strategy",
                json={"artist": artist, "track": track, "genre": "trap"},
                timeout=30
            )
            
            data = response.json()
            
            if data.get('status') == 'success':
                strategy = data.get('strategy', {})
                
                msg = f"""
🎯 **Estrategia Generada por IA**

🎬 Concepto: {strategy.get('concepto_creativo', {}).get('idea_visual', 'N/A')}

�� Hashtags sugeridos:
{', '.join(strategy.get('estrategia_contenido', {}).get('hashtags', [])[:5])}

⏰ Mejor hora: {strategy.get('timing', {}).get('mejor_hora', 'N/A')}

📊 Orden de plataformas:
{', '.join(strategy.get('timing', {}).get('plataformas_orden', []))}
                """
                
                await update.message.reply_text(msg, parse_mode='Markdown')
            else:
                await update.message.reply_text(f"⚠️ Error: {data.get('error', 'Unknown')}")
        
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")

# Inicializar bot
handler = StakazoBotHandler()

def main():
    """Iniciar bot"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN no configurado")
        return
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Registrar comandos
    app.add_handler(CommandHandler("start", handler.start))
    app.add_handler(CommandHandler("status", handler.status))
    app.add_handler(CommandHandler("launch", handler.launch_campaign))
    app.add_handler(CommandHandler("strategy", handler.generate_strategy))
    
    logger.info("🤖 Bot de Telegram iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()
