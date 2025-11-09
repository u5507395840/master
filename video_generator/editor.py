"""
✂️ VIDEO EDITOR - EDICIÓN BÁSICA DE VIDEOS
"""
import logging
from pathlib import Path
from moviepy.editor import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoEditor:
    """Editor de videos para clips cortos"""
    
    @staticmethod
    def trim_video(input_path: str, start: float, end: float, output_path: str) -> str:
        """Recorta video entre start y end (segundos)"""
        try:
            video = VideoFileClip(input_path).subclip(start, end)
            video.write_videofile(output_path, codec='libx264', audio_codec='aac')
            logger.info(f"✅ Video recortado: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"❌ Error recortando video: {e}")
            raise
    
    @staticmethod
    def create_promo_clip(video_path: str, duration: int = 30, output_path: str = None) -> str:
        """Crea clip promocional de X segundos desde el inicio"""
        try:
            video = VideoFileClip(video_path)
            promo = video.subclip(0, min(duration, video.duration))
            
            if not output_path:
                output_path = str(Path(video_path).with_suffix('')) + f"_promo_{duration}s.mp4"
            
            promo.write_videofile(output_path, codec='libx264', audio_codec='aac')
            logger.info(f"✅ Promo clip creado: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"❌ Error creando promo: {e}")
            raise
    
    @staticmethod
    def add_text_overlay(
        video_path: str,
        text: str,
        position: tuple = ('center', 'bottom'),
        duration: float = None,
        output_path: str = None
    ) -> str:
        """Añade texto overlay al video"""
        try:
            video = VideoFileClip(video_path)
            
            txt_clip = TextClip(
                text,
                fontsize=50,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=2
            ).set_position(position).set_duration(duration or video.duration)
            
            final = CompositeVideoClip([video, txt_clip])
            
            if not output_path:
                output_path = str(Path(video_path).with_suffix('')) + "_overlay.mp4"
            
            final.write_videofile(output_path, codec='libx264', audio_codec='aac')
            logger.info(f"✅ Overlay añadido: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"❌ Error añadiendo overlay: {e}")
            raise
