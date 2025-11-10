"""
Copy Generator Component
Generación de copy y captions con OpenAI
"""
import gradio as gr
from typing import List

class CopyGeneratorComponent:
    """Componente para generar copy viral"""
    
    def __init__(self, openai_client=None):
        self.openai = openai_client
    
    def build(self) -> gr.Tab:
        """Construir el tab de generación de copy"""
        
        with gr.Tab("✍️ Generar Copy") as tab:
            
            gr.Markdown("### Generación de Copy Viral con IA")
            gr.Markdown("Genera captions y hashtags optimizados para cada plataforma")
            
            with gr.Row():
                # Columna de inputs
                with gr.Column(scale=1):
                    
                    gr.Markdown("#### 📝 Información del Track")
                    
                    track_input = gr.Textbox(
                        label="🎵 Nombre del Track",
                        placeholder="Ej: Tití Me Preguntó"
                    )
                    
                    artist_input = gr.Textbox(
                        label="🎤 Artista",
                        placeholder="Ej: Bad Bunny"
                    )
                    
                    genre_input = gr.Dropdown(
                        choices=["trap", "reggaeton", "rap", "pop urbano", "dembow"],
                        label="🎸 Género",
                        value="trap"
                    )
                    
                    mood_input = gr.Dropdown(
                        choices=["energético", "romántico", "melancólico", "fiestero"],
                        label="🎭 Mood",
                        value="energético"
                    )
                    
                    gr.Markdown("#### ⚙️ Configuración")
                    
                    platform_input = gr.Radio(
                        choices=["TikTok", "Instagram", "YouTube", "Twitter", "Universal"],
                        label="📱 Plataforma Target",
                        value="TikTok",
                        info="El copy se optimizará para esta plataforma"
                    )
                    
                    count_input = gr.Slider(
                        minimum=1,
                        maximum=10,
                        value=5,
                        step=1,
                        label="🔢 Cantidad de Variantes",
                        info="Cuántos captions diferentes generar"
                    )
                    
                    tone_input = gr.Radio(
                        choices=["casual", "profesional", "juvenil", "provocativo"],
                        label="🎯 Tono",
                        value="juvenil"
                    )
                    
                    include_cta = gr.Checkbox(
                        label="📢 Incluir Call-to-Action",
                        value=True
                    )
                    
                    include_emojis = gr.Checkbox(
                        label="😀 Incluir Emojis",
                        value=True
                    )
                    
                    # Botones
                    generate_btn = gr.Button(
                        "✨ GENERAR COPY CON IA",
                        variant="primary",
                        size="lg"
                    )
                    
                    hashtags_btn = gr.Button(
                        "#️⃣ Solo Hashtags",
                        variant="secondary"
                    )
                
                # Columna de resultados
                with gr.Column(scale=1):
                    
                    gr.Markdown("#### 📄 Copy Generado")
                    
                    copy_output = gr.Textbox(
                        label="Captions Listos para Usar",
                        lines=30,
                        max_lines=40,
                        interactive=False,
                        show_copy_button=True
                    )
                    
                    with gr.Row():
                        copy_btn = gr.Button("📋 Copiar Todo", size="sm")
                        save_btn = gr.Button("💾 Guardar", size="sm")
            
            # Conectar eventos
            generate_btn.click(
                fn=self.generate_complete_copy,
                inputs=[
                    track_input,
                    artist_input,
                    genre_input,
                    mood_input,
                    platform_input,
                    count_input,
                    tone_input,
                    include_cta,
                    include_emojis
                ],
                outputs=copy_output
            )
            
            hashtags_btn.click(
                fn=self.generate_only_hashtags,
                inputs=[genre_input, mood_input, platform_input],
                outputs=copy_output
            )
        
        return tab
    
    def generate_complete_copy(
        self,
        track: str,
        artist: str,
        genre: str,
        mood: str,
        platform: str,
        count: int,
        tone: str,
        include_cta: bool,
        include_emojis: bool
    ) -> str:
        """Generar copy completo con todos los parámetros"""
        
        if not track or not artist:
            return "❌ ERROR: Completa al menos el Track y Artista"
        
        # Generar captions
        if self.openai:
            try:
                captions = self._generate_with_openai(
                    track, artist, genre, mood, platform, 
                    count, tone, include_cta, include_emojis
                )
            except Exception as e:
                captions = self._generate_fallback(
                    track, artist, genre, platform, count
                )
        else:
            captions = self._generate_fallback(
                track, artist, genre, platform, count
            )
        
        # Generar hashtags
        hashtags = self._generate_hashtags(genre, mood, platform)
        
        # Formatear resultado
        result = self._format_copy_result(
            track, artist, genre, platform, captions, hashtags
        )
        
        return result
    
    def generate_only_hashtags(
        self,
        genre: str,
        mood: str,
        platform: str
    ) -> str:
        """Generar solo hashtags"""
        
        hashtags = self._generate_hashtags(genre, mood, platform)
        
        result = f"""
#️⃣ HASHTAGS GENERADOS

Género: {genre}
Mood: {mood}
Plataforma: {platform}

════════════════════════════════════════

{' '.join(hashtags)}

════════════════════════════════════════

💡 TIPS DE USO:

• Usa 5-10 hashtags por post
• Mezcla hashtags populares con nicho
• El primer hashtag es el más importante
• Varía los hashtags entre posts

Copia y pega directamente en tu post.
        """
        
        return result
    
    def _generate_with_openai(
        self, track, artist, genre, mood, platform, 
        count, tone, include_cta, include_emojis
    ) -> List[str]:
        """Generar captions usando OpenAI"""
        
        # Construir prompt optimizado
        prompt = self._build_prompt(
            track, artist, genre, mood, platform,
            tone, include_cta, include_emojis
        )
        
        captions = self.openai.generate_captions(
            track_name=track,
            artist=artist,
            genre=genre,
            platform=platform.lower(),
            count=count
        )
        
        return captions
    
    def _generate_fallback(
        self, track, artist, genre, platform, count
    ) -> List[str]:
        """Fallback sin OpenAI"""
        
        templates = [
            f"🔥 {track} - {artist} | Nuevo {genre} disponible YA",
            f"Este tema está 🔥🔥🔥 | {track} de {artist}",
            f"📢 NUEVO {genre.upper()} | {artist} acaba de soltar {track}",
            f"{artist} 🎵 {track} | Dale play ahora mismo",
            f"¿Ya escuchaste {track}? {artist} la rompió 🔥",
            f"Nuevo {genre} de {artist}: {track} 🎧",
            f"🎵 {track} | {artist} | Ya disponible en todas las plataformas",
            f"No pares de escuchar {track} de {artist} 🔁",
            f"{artist} - {track} | El {genre} que necesitabas 💯",
            f"LOOP MODE: {track} by {artist} 🔄🔥"
        ]
        
        return templates[:count]
    
    def _generate_hashtags(
        self, genre: str, mood: str, platform: str
    ) -> List[str]:
        """Generar hashtags relevantes"""
        
        if self.openai:
            try:
                return self.openai.generate_hashtags(genre, mood)
            except:
                pass
        
        # Hashtags base
        base_tags = [
            "#music",
            "#newmusic",
            f"#{genre}",
            "#viral",
            "#fyp"
        ]
        
        # Hashtags por género
        genre_tags = {
            "trap": ["#trap", "#trapmusic", "#trapbeats", "#traplife"],
            "reggaeton": ["#reggaeton", "#perreo", "#latinmusic", "#urbanolatino"],
            "rap": ["#rap", "#hiphop", "#rapper", "#bars"],
            "pop urbano": ["#popurbano", "#urbanpop", "#latinpop"],
            "dembow": ["#dembow", "#dembowdominicano", "#urbano"]
        }
        
        # Hashtags por plataforma
        platform_tags = {
            "TikTok": ["#tiktok", "#tiktokviral", "#tiktokmusic"],
            "Instagram": ["#instagrammusic", "#musicvideo", "#instamusic"],
            "YouTube": ["#youtubemusic", "#musicvideo", "#newvideo"]
        }
        
        # Combinar
        all_tags = base_tags.copy()
        all_tags.extend(genre_tags.get(genre, []))
        all_tags.extend(platform_tags.get(platform, []))
        
        return all_tags[:15]
    
    def _build_prompt(
        self, track, artist, genre, mood, platform,
        tone, include_cta, include_emojis
    ):
        """Construir prompt optimizado para OpenAI"""
        
        prompt = f"""
Genera captions virales para {platform} promocionando:
Track: "{track}" de {artist}
Género: {genre}
Mood: {mood}
Tono: {tone}

Requisitos:
- Longitud adecuada para {platform}
- Tono {tone}
"""
        
        if include_cta:
            prompt += "- Incluir call-to-action sutil\n"
        
        if include_emojis:
            prompt += "- Usar emojis relevantes\n"
        else:
            prompt += "- SIN emojis\n"
        
        prompt += "\nSolo devuelve los captions, uno por línea."
        
        return prompt
    
    def _format_copy_result(
        self, track, artist, genre, platform, captions, hashtags
    ) -> str:
        """Formatear resultado final"""
        
        result = f"""
✅ COPY GENERADO CON IA

════════════════════════════════════════════════════════════════

📋 INFORMACIÓN

🎵 Track: {track}
🎤 Artista: {artist}
🎸 Género: {genre}
📱 Optimizado para: {platform}

════════════════════════════════════════════════════════════════

✍️ CAPTIONS ({len(captions)} variantes)

"""
        
        for i, caption in enumerate(captions, 1):
            result += f"\n{i}️⃣  {caption}\n"
        
        result += f"""

════════════════════════════════════════════════════════════════

#️⃣ HASHTAGS RECOMENDADOS

{' '.join(hashtags[:10])}

════════════════════════════════════════════════════════════════

💡 TIPS DE USO

• Rota entre diferentes variantes para cada post
• El copy #1 suele tener mejor performance
• Adapta ligeramente según tu audiencia
• Testea con/sin hashtags para ver qué funciona mejor

📋 TODO LISTO PARA COPIAR Y PEGAR

Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        """
        
        return result

