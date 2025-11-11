"""Telegram Bot - Control remoto REAL del sistema"""
import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

system_state = {"active_campaigns": 0, "total_reach": 0, "last_launch": None, "status": "idle"}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("�� Nueva Campaña", callback_data='new_campaign')],
                [InlineKeyboardButton("📊 Ver Métricas", callback_data='metrics')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎵 *Stakazo Control Bot*\n\n/nueva /metricas /status", 
                                     parse_mode='Markdown', reply_markup=reply_markup)

async def new_campaign_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    system_state["active_campaigns"] += 1
    system_state["last_launch"] = datetime.now().isoformat()
    system_state["status"] = "active"
    await update.message.reply_text(f"✅ Campaña #{system_state['active_campaigns']} iniciada")

async def metrics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"📊 *Métricas*\n\n🎯 Campañas: {system_state['active_campaigns']}\n⚡ Estado: {system_state['status']}"
    if update.message:
        await update.message.reply_text(msg, parse_mode='Markdown')
    else:
        await update.callback_query.message.edit_text(msg, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'new_campaign':
        system_state["active_campaigns"] += 1
        await query.message.reply_text(f"✅ Campaña iniciada")
    elif query.data == 'metrics':
        await metrics_command(update, context)

# --- Módulo Listener ---
def listen_for_links(update: Update):
    # Detecta links de YouTube/Instagram en mensajes
    text = update.message.text if update.message else ""
    if "youtube.com" in text or "youtu.be" in text or "instagram.com" in text:
        # Consulta al orquestador ML para priorizar acción
        try:
            # Conversacional y priorización por GPT-3.5
            priority = requests.get("http://localhost:8000/get_priority_content?model=gpt-3.5-turbo").json()
            payload = {
                "user": update.effective_user.id,
                "text": text,
                "group": update.effective_chat.id,
                "priority": priority,
                "model": "gpt-3.5-turbo"
            }
            requests.post("http://localhost:8000/register_support_request", json=payload)
            # Ejecuta acción priorizada automáticamente
            if priority.get("action"):
                execute_interaction(text, priority.get("platform", "youtube"), update.effective_user.id)
        except Exception as e:
            logger.error(f"Error en integración IA/ML: {e}")

# --- Módulo Executor ---
def execute_interaction(link, platform, user_id):
    # Gestiona la acción automática (like, comentario, etc.)
    # Ejemplo: notificar al backend para ejecutar acción
    try:
        payload = {"link": link, "platform": platform, "user": user_id}
        requests.post("http://localhost:8000/execute_interaction", json=payload)
    except Exception as e:
        logger.error(f"Error ejecutando interacción: {e}")

# --- Módulo Priorización ---
def get_priority_content():
    # Consulta al orquestador qué contenido empujar
    try:
        resp = requests.get("http://localhost:8000/get_priority_content")
        return resp.json()
    except Exception:
        return {}

# --- Módulo Registro y Métricas ---
def log_interaction(data):
    # Guarda interacción en la base de datos (Supabase/MongoDB)
    try:
        requests.post("http://localhost:8000/log_interaction", json=data)
    except Exception as e:
        logger.error(f"Error registrando métrica: {e}")

# --- Módulo Interacción Emocional ---
def send_emotional_message(update: Update, tipo="youtube"):
    # Mensajes variados y comportamiento humano según métricas históricas
    mensajes = {
        "youtube": [
            "🔥 Nuevo videoclip, apóyame con like y comenta 💬🔥",
            "Bro, dale una escuchada a este clip, la rompemos 💣",
            "¿Quién se anima a comentar algo original?",
            "Si te mola, suscríbete y comparte, ¡apoyo mutuo!",
            "Hoy toca apoyar a los que más comentan, ¿te sumas?"
        ],
        "instagram": [
            "💥 Subí nuevo reel, deja un ❤️ y te devuelvo apoyo.",
            "Gracias a todos los que están compartiendo mi música en stories 🔁",
            "¿Quién quiere full apoyo en Insta hoy?",
            "Si te gusta, guarda la publicación y comenta tu opinión",
            "Hoy toca apoyar reels virales, ¿te apuntas?"
        ]
    }
    import random, time
    # Simula delay humano y variación textual
    delay = random.uniform(3, 20)
    time.sleep(delay)
    # Selecciona mensaje según métricas históricas (simulado)
    try:
        resp = requests.get("http://localhost:8000/get_human_metrics")
        metric = resp.json().get("top_message", None)
        if metric:
            msg = metric
        else:
            msg = random.choice(mensajes.get(tipo, ["Apoya este contenido!"]))
    except Exception:
        msg = random.choice(mensajes.get(tipo, ["Apoya este contenido!"]))
    if update.message:
        update.message.reply_text(msg)

# --- Módulo Expansión Automática ---
def expand_to_satellites():
    # Añade cuentas satélite y gestiona roles
    try:
        requests.post("http://localhost:8000/expand_satellites", json={})
    except Exception as e:
        logger.error(f"Error expandiendo satélites: {e}")

def main():
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN no configurado")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("nueva", new_campaign_command))
    app.add_handler(CommandHandler("metricas", metrics_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("🤖 Bot iniciado")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
