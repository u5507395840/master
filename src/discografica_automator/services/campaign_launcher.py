import logging
import time
import os

# --- Importaciones Corregidas ---
# Se importan las funciones específicas en lugar de un objeto 'db'
from discografica_automator.core.database import get_campaign_by_id, update_campaign_status, CampaignStatus
from discografica_automator.services import copy_generator, video_generator
from discografica_automator.integrations import meta_poster, tiktok_poster, youtube_uploader

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DUMMY_MODE = os.getenv('DUMMY_MODE', 'false').lower() in ('true', '1', 't')

def launch_campaign(campaign_id: str):
    """
    Orquesta el ciclo de vida completo de una campaña.
    """
    logging.info(f"Iniciando lanzamiento de campaña: {campaign_id}")
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        logging.error(f"Campaña {campaign_id} no encontrada al iniciar el lanzamiento.")
        return

    try:
        # 1. Generar copys
        update_campaign_status(campaign_id, CampaignStatus.GENERATING_CAPTIONS)
        logging.info(f"Generando captions para la campaña {campaign_id}...")
        captions = copy_generator.generate_captions(campaign.track, campaign.artist)
        logging.info(f"Captions generados para {campaign_id}: {captions}")

        # 2. Generar video
        update_campaign_status(campaign_id, CampaignStatus.GENERATING_VIDEO)
        logging.info(f"Generando video para la campaña {campaign_id}...")
        video_path = video_generator.generate_video(campaign.video_prompt)
        logging.info(f"Video generado para {campaign_id} en: {video_path}")

        # 3. Distribuir en plataformas
        update_campaign_status(campaign_id, CampaignStatus.DISTRIBUTING)
        for platform, caption in captions.items():
            logging.info(f"Distribuyendo en la plataforma: {platform}")
            if platform == "instagram" or platform == "facebook":
                meta_poster.post_to_meta(platform, video_path, caption)
            elif platform == "tiktok":
                tiktok_poster.post_to_tiktok(video_path, caption)
            elif platform == "youtube":
                youtube_uploader.upload_video(video_path, f"{campaign.artist} - {campaign.track}", caption)
        
        # 4. Marcar como completado
        update_campaign_status(campaign_id, CampaignStatus.COMPLETED)
        logging.info(f"Lanzamiento de campaña '{campaign_id}' completado exitosamente.")

    except Exception as e:
        logging.error(f"Error catastrófico durante el lanzamiento de la campaña {campaign_id}: {e}", exc_info=True)
        update_campaign_status(campaign_id, CampaignStatus.FAILED)

