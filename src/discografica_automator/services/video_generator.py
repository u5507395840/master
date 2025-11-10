"""
Placeholder para el Video Generator.
En una implementación real, usaría modelos como LongCat-Video.
"""
import logging
import time
import os

logger = logging.getLogger(__name__)

def generate_video(prompt: str, output_dir: str = "data/videos") -> str:
    """Simula la generación de un video y retorna la ruta al archivo."""
    os.makedirs(output_dir, exist_ok=True)
    
    video_filename = f"video_{int(time.time())}.mp4"
    video_path = os.path.join(output_dir, video_filename)
    
    logger.info(f"[DUMMY] Generando video para el prompt: '{prompt[:50]}...'")
    time.sleep(2) # Simular tiempo de renderizado
    
    # Crear un archivo de video falso
    with open(video_path, "w") as f:
        f.write(f"Fake video content for prompt: {prompt}")
        
    logger.info(f"[DUMMY] Video generado en: {video_path}")
    return video_path
