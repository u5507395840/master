"""Copy Generator - OpenAI REAL"""
import os
import openai
import json
from typing import List

class CopyGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=self.api_key) if self.api_key else None
    
    def generate_captions(self, track_name: str, artist: str, genre: str = "trap") -> dict:
        """Genera un diccionario de captions para varias plataformas."""
        if not self.client:
            base_caption = f"🔥 {track_name} - {artist} #viral #music"
            return {
                "instagram": base_caption,
                "facebook": base_caption,
                "tiktok": base_caption,
                "youtube": f"Escucha '{track_name}' de {artist} ya disponible. #newmusic #{genre}"
            }
        
        try:
            prompt = (
                f"Eres un experto en marketing musical viral. Genera 4 captions cortos y virales para promocionar "
                f"la canción '{track_name}' de {artist} (género: {genre}). "
                "Devuelve un JSON con claves 'instagram', 'tiktok', 'facebook', 'youtube'. "
                "Ejemplo de formato: {\"instagram\": \"texto para insta...\", \"tiktok\": \"texto para tiktok...\"}"
            )
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "Eres un experto en marketing musical que siempre devuelve JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.9
            )
            
            captions = json.loads(response.choices[0].message.content)
            return captions
        except Exception as e:
            print(f"Error al generar captions con OpenAI: {e}")
            base_caption = f"🔥 {track_name} YA disponible | {artist} #newmusic"
            return {
                "instagram": base_caption,
                "facebook": base_caption,
                "tiktok": base_caption,
                "youtube": f"Videoclip oficial de '{track_name}' por {artist}."
            }
    
    def generate_hashtags(self, genre: str, mood: str = "energetic") -> List[str]:
        if not self.client:
            return ["#music", "#newmusic", f"#{genre}", "#viral", "#fyp"]
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"10 hashtags virales para música {genre}. Solo hashtags, separados por comas."}],
                max_tokens=100)
            return [tag.strip() for tag in response.choices[0].message.content.split(',')][:10]
        except:
            return ["#music", "#newmusic", f"#{genre}", "#viral"]

copy_generator = CopyGenerator()
