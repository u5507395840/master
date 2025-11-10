"""
Script principal para ejecutar el ciclo de decisión de marketing.
"""
import sys
import os

# Añadir el directorio 'src' al PYTHONPATH para encontrar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import logging
from discografica_automator.services.orchestrator import orchestrator
from discografica_automator.integrations.n8n_client import n8n_client
from analytics_engine import get_youtube_performance_report

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_decision_cycle():
    """
    Ejecuta un ciclo completo de decisión y ejecución de campañas.
    """
    logging.info("🚀 Iniciando nuevo ciclo de decisión de marketing...")

    # 1. Obtener datos de rendimiento (simulados)
    logging.info("Paso 1: Obteniendo informe de rendimiento de campañas anteriores...")
    performance_report = get_youtube_performance_report(days=30)
    if not performance_report:
        logging.error("No se pudo obtener el informe de rendimiento. Abortando el ciclo.")
        return

    youtube_channel = performance_report.get("youtube_channel_url", "URL_NO_ENCONTRADA")
    logging.info(f"Informe obtenido. El objetivo es dirigir tráfico a: {youtube_channel}")

    # 2. Pedir a OpenAI que decida la estrategia
    total_budget = 100.0  # Presupuesto para la nueva fase
    logging.info(f"Paso 2: Solicitando estrategia a OpenAI con un presupuesto de {total_budget} EUR...")
    
    strategy_plan = orchestrator.decide_meta_ads_strategy(
        performance_data=performance_report,
        total_budget=total_budget,
        youtube_channel_url=youtube_channel
    )

    if not strategy_plan or "campaign_plan" not in strategy_plan:
        logging.error("No se pudo generar un plan de estrategia válido. Abortando el ciclo.")
        return
    
    logging.info("✅ Estrategia de Meta Ads generada por OpenAI:")
    for i, campaign in enumerate(strategy_plan["campaign_plan"]):
        logging.info(f"  - Campaña Satélite {i+1}: {campaign['campaign_name']} | Presupuesto: {campaign['budget_eur']} EUR")

    # 3. Ejecutar el plan de campaña a través de n8n
    logging.info("Paso 3: Enviando el plan de campaña a n8n para su ejecución...")
    success = n8n_client.execute_campaign_plan(strategy_plan)

    if success:
        logging.info("🎉 Ciclo de decisión completado. n8n ha recibido el plan y comenzará la ejecución.")
    else:
        logging.error("❌ Falló el envío del plan a n8n. El ciclo no se completó.")

if __name__ == "__main__":
    # Para ejecutar este script, asegúrate de tener las variables de entorno configuradas:
    # OPENAI_API_KEY="tu_api_key"
    # N8N_META_ADS_WEBHOOK_URL="tu_webhook_url"
    run_decision_cycle()
