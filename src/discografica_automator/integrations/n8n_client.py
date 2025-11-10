"""
Cliente para interactuar con los webhooks de n8n.
"""
import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class N8NClient:
    def __init__(self):
        self.n8n_webhook_url = os.getenv("N8N_META_ADS_WEBHOOK_URL")
        if not self.n8n_webhook_url:
            logger.warning("⚠️ N8N_META_ADS_WEBHOOK_URL no está configurada. No se podrán ejecutar campañas.")

    def execute_campaign_plan(self, campaign_plan: dict) -> bool:
        """
        Envía el plan de campañas a un webhook de n8n para su ejecución.
        """
        if not self.n8n_webhook_url:
            logger.error("No se puede ejecutar el plan de campaña: la URL del webhook de n8n no está configurada.")
            return False

        if "campaign_plan" not in campaign_plan or not isinstance(campaign_plan["campaign_plan"], list):
            logger.error("El plan de campaña tiene un formato inválido. Se esperaba una clave 'campaign_plan' con una lista.")
            return False

        logger.info(f"Enviando plan de {len(campaign_plan['campaign_plan'])} campañas al webhook de n8n...")

        try:
            response = requests.post(self.n8n_webhook_url, json=campaign_plan)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP (4xx o 5xx)
            
            logger.info(f"✅ Plan de campaña enviado a n8n exitosamente. Respuesta: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al enviar el plan de campaña a n8n: {e}")
            return False

# Instancia global
n8n_client = N8NClient()
