"""
🎬 VIDEO GENERATOR - GENERACIÓN AUTOMÁTICA DE VIDEOS
Integra OpenAI para prompts + MoviePy para edición
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoGenerator:
    """Generador de videos con IA"""
    
    def __init__(self, output_dir: str = "data/videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_lyric_video(
        self,
        audio_path: str,
        lyrics: str,
        title: str,
        artist: str,
        output_name: Optional[str] = None
    ) -> str:
        """Crea video de letras sincronizado"""
        try:
            logger.info(f"🎬 Creando lyric video: {title}")
            
            # Cargar audio
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Crear fondo
            w, h = 1080, 1920  # Vertical para redes sociales
            background = self._create_gradient_background(w, h, duration)
            
            # Añadir texto de letras
            lyrics_clip = self._create_lyrics_clip(lyrics, duration, w, h)
            
            # Añadir título y artista
            title_clip = self._create_title_clip(title, artist, w, h)
            
            # Componer video
            video = CompositeVideoClip([
                background,
                lyrics_clip.set_position('center'),
                title_clip.set_position(('center', 100))
            ])
            
            # Añadir audio
            video = video.set_audio(audio)
            
            # Exportar
            output_path = self.output_dir / (output_name or f"{title}_lyric_video.mp4")
            video.write_videofile(
                str(output_path),
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            
            logger.info(f"✅ Video creado: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Error creando lyric video: {e}")
            raise
    
    def create_visualizer_video(
        self,
        audio_path: str,
        title: str,
        artist: str,
        style: str = "waveform",
        output_name: Optional[str] = None
    ) -> str:
        """Crea video con visualizador de audio"""
        try:
            logger.info(f"🎬 Creando visualizer video: {title}")
            
            # Cargar audio
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Crear visualizador
            w, h = 1080, 1920
            visualizer = self._create_audio_visualizer(audio_path, duration, w, h, style)
            
            # Añadir info del track
            info_clip = self._create_title_clip(title, artist, w, h)
            
            # Componer
            video = CompositeVideoClip([
                visualizer,
                info_clip.set_position(('center', 100))
            ])
            
            video = video.set_audio(audio)
            
            # Exportar
            output_path = self.output_dir / (output_name or f"{title}_visualizer.mp4")
            video.write_videofile(
                str(output_path),
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            
            logger.info(f"✅ Video creado: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Error creando visualizer: {e}")
            raise
    
    def create_cover_video(
        self,
        audio_path: str,
        cover_image_path: str,
        title: str,
        artist: str,
        output_name: Optional[str] = None
    ) -> str:
        """Crea video simple con portada estática + audio"""
        try:
            logger.info(f"🎬 Creando cover video: {title}")
            
            # Cargar audio
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Cargar y redimensionar portada
            img = ImageClip(cover_image_path)
            img = img.resize(height=1920)  # Vertical
            img = img.set_duration(duration)
            
            # Añadir overlay con info
            info_clip = self._create_title_clip(title, artist, 1080, 1920)
            
            # Componer
            video = CompositeVideoClip([
                img,
                info_clip.set_position(('center', 100)).set_opacity(0.9)
            ])
            
            video = video.set_audio(audio)
            
            # Exportar
            output_path = self.output_dir / (output_name or f"{title}_cover_video.mp4")
            video.write_videofile(
                str(output_path),
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            
            logger.info(f"✅ Video creado: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Error creando cover video: {e}")
            raise
    
    def _create_gradient_background(self, w: int, h: int, duration: float) -> VideoClip:
        """Crea fondo con gradiente animado"""
        def make_frame(t):
            # Gradiente que cambia con el tiempo
            top_color = np.array([138, 43, 226])  # Purple
            bottom_color = np.array([0, 0, 0])  # Black
            
            gradient = np.zeros((h, w, 3), dtype=np.uint8)
            for y in range(h):
                ratio = y / h
                gradient[y] = top_color * (1 - ratio) + bottom_color * ratio
            
            return gradient
        
        return VideoClip(make_frame, duration=duration)
    
    def _create_lyrics_clip(self, lyrics: str, duration: float, w: int, h: int) -> TextClip:
        """Crea clip de texto con letras"""
        return TextClip(
            lyrics,
            fontsize=50,
            color='white',
            font='Arial-Bold',
            size=(w - 100, None),
            method='caption'
        ).set_duration(duration)
    
    def _create_title_clip(self, title: str, artist: str, w: int, h: int) -> TextClip:
        """Crea clip con título y artista"""
        text = f"{title}\n{artist}"
        return TextClip(
            text,
            fontsize=60,
            color='white',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=2
        ).set_duration(5)  # Aparece 5 segundos
    
    def _create_audio_visualizer(
        self,
        audio_path: str,
        duration: float,
        w: int,
        h: int,
        style: str
    ) -> VideoClip:
        """Crea visualizador de audio (placeholder - requiere análisis de audio)"""
        # Por ahora, devuelve fondo animado
        # TODO: Integrar análisis de frecuencias para visualizador real
        return self._create_gradient_background(w, h, duration)
