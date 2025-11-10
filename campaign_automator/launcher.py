"""
Campaign Launcher - Orquestador de Campañas
Automatiza el proceso completo de lanzamiento de una campaña musical.
"""
import os
import logging
import time
from typing import Dict

# Módulos del sistema
from core.database import db
from orchestrator_ml.copy_generator import copy_generator
from orchestrator_ml.video_generator import generate_video_from_prompt
from integrations import meta_poster, tiktok_poster, youtube_uploader

logger = logging.getLogger(__name__)

class CampaignLauncher:
    """Orquesta el lanzamiento de campañas de principio a fin."""

    def __init__(self):
        self.dummy_mode = os.getenv("DUMMY_MODE", "true").lower() == "true"
        if self.dummy_mode:
            logger.warning("El lanzador de campañas está operando en DUMMY_MODE. No se realizarán publicaciones reales.")

    def launch_campaign(self, campaign_id: str) -> bool:
        """
        Ejecuta el flujo completo de lanzamiento para una campaña existente en la DB.
        
        Returns:
            bool: True si el lanzamiento fue exitoso, False en caso contrario.
        """
        logger.info(f"🚀 Iniciando lanzamiento de campaña: {campaign_id}")

        campaign = db.get_campaign(campaign_id)
        if not campaign:
            logger.error(f"Campaña '{campaign_id}' no encontrada en la base de datos. Abortando.")
            return False
        
        db.update_campaign_status(campaign_id, "processing")
        db.log("INFO", "Launcher", f"Campaña '{campaign_id}' en estado 'processing'.")

        try:
            campaign = self._generate_creative_assets(campaign)
            publication_results = self._distribute_to_platforms(campaign)
            
            if 'metrics' not in campaign or campaign['metrics'] is None:
                campaign['metrics'] = {}
            campaign['metrics']['publication_results'] = publication_results
            db.save_campaign(campaign)

            final_status = "active" if any(res.get('status') == 'success' for res in publication_results.values()) else "failed"
            db.update_campaign_status(campaign_id, final_status)
            db.log("INFO", "Launcher", f"Campaña '{campaign_id}' finalizada con estado '{final_status}'.")
            
            logger.info(f"✅ Lanzamiento de campaña '{campaign_id}' completado con estado '{final_status}'.")
            return final_status != "failed"

        except Exception as e:
            logger.critical(f"Error crítico durante el lanzamiento de la campaña '{campaign_id}': {e}", exc_info=True)
            db.update_campaign_status(campaign_id, "failed")
            db.log("ERROR", "Launcher", f"Lanzamiento fallido para '{campaign_id}': {e}")
            return False

    def _generate_creative_assets(self, campaign: Dict) -> Dict:
        """Genera captions, hashtags y video si no existen."""
        if not campaign.get('captions'):
            logger.info(f"Generando captions para la campaña '{campaign['id']}'...")
            campaign['captions'] = copy_generator.generate_captions(
                track_name=campaign['track'], artist=campaign['artist'],
                genre=campaign['genre'], mood=campaign.get('mood', 'energetic'), count=3
            )
            db.save_campaign(campaign)
        
        if campaign.get('video_prompt') and not campaign.get('video_url'):
            logger.info(f"Generando video para la campaña '{campaign['id']}'...")
            video_path = generate_video_from_prompt(campaign['video_prompt'])
            campaign['video_url'] = video_path
            db.save_campaign(campaign)
            
        return campaign

    def _distribute_to_platforms(self, campaign: Dict) -> Dict:
        """Publica el contenido en las plataformas seleccionadas."""
        results = {}
        video_path = campaign.get('video_url')
        caption = campaign.get('captions', [""])[0]

        if not video_path:
            logger.error("No hay video para publicar. Abortando distribución.")
            return results

        for platform in campaign.get('platforms', []):
            logger.info(f"Distribuyendo en la plataforma: {platform}")
            try:
                if self.dummy_mode:
                    results[platform] = {"status": "success", "post_id": f"dummy_{platform}_123"}
                    time.sleep(1)
                    continue

                if platform.lower() == 'instagram':
                    token = os.getenv("META_ACCESS_TOKEN")
                    if not token: raise ValueError("META_ACCESS_TOKEN no configurado.")
                    results[platform] = meta_poster.post_reel(video_path, caption, token)
                elif platform.lower() == 'tiktok':
                    api_key = os.getenv("TIKTOK_API_KEY")
                    if not api_key: raise ValueError("TIKTOK_API_KEY no configurado.")
                    results[platform] = tiktok_poster.post_video(video_path, caption, api_key)
                elif platform.lower() == 'youtube':
                    creds = None
                    results[platform] = youtube_uploader.upload_short(video_path, campaign['track'], caption, creds)
                
            except Exception as e:
                logger.error(f"Fallo al publicar en {platform}: {e}")
                results[platform] = {"status": "failed", "error": str(e)}
        
        return results

campaign_launcher = CampaignLauncher()
