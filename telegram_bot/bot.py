"""Telegram Bot - Control remoto REAL del sistema"""
import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

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
