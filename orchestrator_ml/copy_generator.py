"""Copy Generator - OpenAI REAL"""
import os
import openai
from typing import List

class CopyGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=self.api_key) if self.api_key else None
    
    def generate_captions(self, track_name: str, artist: str, genre: str = "trap", 
                         platform: str = "tiktok", count: int = 3) -> List[str]:
        if not self.client:
            return [f"🔥 {track_name} - {artist} #viral #music",
                    f"Este tema está 🔥 | {track_name}",
                    f"📢 NUEVO | {artist} - {track_name}"]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "Eres experto en marketing musical viral."},
                         {"role": "user", "content": f"Genera {count} captions virales cortos para {platform} "
                          f"promocionando '{track_name}' de {artist} (género: {genre})"}],
                max_tokens=300, temperature=0.9)
            captions = [c.strip() for c in response.choices[0].message.content.strip().split('\n') if c.strip()]
            return captions[:count]
        except Exception as e:
            print(f"Error: {e}")
            return [f"🔥 {track_name} YA disponible | {artist} #newmusic"]
    
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
