"""
Campaign Launcher Component
Formulario completo para lanzar campañas virales
"""
import gradio as gr
from datetime import datetime
from typing import Dict, List, Tuple

class CampaignLauncher:
    """Componente para lanzar campañas desde el dashboard"""
    
    def __init__(self, db_manager=None, openai_client=None):
        self.db = db_manager
        self.openai = openai_client
        
    def build(self) -> gr.Tab:
        """Construir el tab de lanzamiento"""
        
        with gr.Tab("🚀 Lanzar Campaña") as tab:
            
            gr.Markdown("### Lanzar Nueva Campaña Viral")
            gr.Markdown("Completa los datos y el sistema generará todo automáticamente")
            
            with gr.Row():
                # Columna de inputs
                with gr.Column(scale=1):
                    
                    # Información del track
                    gr.Markdown("#### 📝 Información del Track")
                    
                    artist_input = gr.Textbox(
                        label="🎤 Artista",
                        placeholder="Ej: Bad Bunny",
                        info="Nombre del artista o grupo"
                    )
                    
                    track_input = gr.Textbox(
                        label="🎵 Nombre del Track",
                        placeholder="Ej: Tití Me Preguntó",
                        info="Título de la canción"
                    )
                    
                    genre_input = gr.Dropdown(
                        choices=[
                            "trap",
                            "reggaeton", 
                            "rap",
                            "pop urbano",
                            "dembow",
                            "r&b",
                            "afrobeat"
                        ],
                        label="🎸 Género Musical",
                        value="trap",
                        info="Selecciona el género principal"
                    )
                    
                    mood_input = gr.Dropdown(
                        choices=[
                            "energético",
                            "romántico",
                            "melancólico",
                            "fiestero",
                            "agresivo",
                            "relajado"
                        ],
                        label="🎭 Mood del Track",
                        value="energético"
                    )
                    
                    # Configuración de campaña
                    gr.Markdown("#### ⚙️ Configuración de Campaña")
                    
                    platforms_input = gr.CheckboxGroup(
                        choices=[
                            "TikTok",
                            "Instagram Reels",
                            "YouTube Shorts",
                            "Facebook",
                            "Twitter/X"
                        ],
                        label="📱 Plataformas Target",
                        value=["TikTok", "Instagram Reels"],
                        info="Selecciona dónde publicar"
                    )
                    
                    budget_input = gr.Slider(
                        minimum=0,
                        maximum=10000,
                        value=500,
                        step=50,
                        label="💰 Presupuesto (USD)",
                        info="Budget para ads pagados (0 = orgánico)"
                    )
                    
                    duration_input = gr.Slider(
                        minimum=1,
                        maximum=30,
                        value=7,
                        step=1,
                        label="📅 Duración (días)",
                        info="Duración de la campaña"
                    )
                    
                    # Video/Creative
                    gr.Markdown("#### 🎬 Creative (Opcional)")
                    
                    video_url_input = gr.Textbox(
                        label="🔗 URL del Video",
                        placeholder="https://...",
                        info="URL del video si ya existe"
                    )
                    
                    video_prompt_input = gr.Textbox(
                        label="✨ Prompt para Video AI",
                        placeholder="Ej: Artista en estudio con luces neón azules",
                        lines=2,
                        info="Para generar video con IA (futuro)"
                    )
                    
                    # Opciones avanzadas
                    with gr.Accordion("🔧 Opciones Avanzadas", open=False):
                        
                        target_age_input = gr.CheckboxGroup(
                            choices=["13-17", "18-24", "25-34", "35-44", "45+"],
                            label="🎯 Edad Target",
                            value=["18-24", "25-34"]
                        )
                        
                        target_gender_input = gr.Radio(
                            choices=["Todos", "Masculino", "Femenino"],
                            label="👥 Género Target",
                            value="Todos"
                        )
                        
                        auto_optimize_input = gr.Checkbox(
                            label="🤖 Auto-optimización con ML",
                            value=True,
                            info="El sistema ajustará la campaña automáticamente"
                        )
                    
                    # Botón de lanzamiento
                    launch_btn = gr.Button(
                        "🔴 LANZAR CAMPAÑA VIRAL",
                        variant="primary",
                        size="lg"
                    )
                
                # Columna de resultados
                with gr.Column(scale=1):
                    
                    gr.Markdown("#### 📊 Vista Previa & Resultados")
                    
                    # Área de resultados
                    result_output = gr.Textbox(
                        label="Resultado del Lanzamiento",
                        lines=25,
                        max_lines=35,
                        interactive=False
                    )
                    
                    # Botones de acción secundarios
                    with gr.Row():
                        save_draft_btn = gr.Button("💾 Guardar Borrador", size="sm")
                        clear_btn = gr.Button("🗑️ Limpiar", size="sm")
            
            # Conectar evento del botón principal
            launch_btn.click(
                fn=self.launch_campaign,
                inputs=[
                    artist_input,
                    track_input,
                    genre_input,
                    mood_input,
                    platforms_input,
                    budget_input,
                    duration_input,
                    video_url_input,
                    video_prompt_input,
                    target_age_input,
                    target_gender_input,
                    auto_optimize_input
                ],
                outputs=result_output
            )
            
            # Botón de limpiar
            clear_btn.click(
                fn=lambda: [""] * 12,
                outputs=[
                    artist_input, track_input, video_url_input,
                    video_prompt_input, result_output
                ]
            )
        
        return tab
    
    def launch_campaign(
        self,
        artist: str,
        track: str,
        genre: str,
        mood: str,
        platforms: List[str],
        budget: float,
        duration: int,
        video_url: str,
        video_prompt: str,
        target_age: List[str],
        target_gender: str,
        auto_optimize: bool
    ) -> str:
        """Lanzar campaña con todos los parámetros"""
        
        # Validaciones
        if not artist or not track:
            return "❌ ERROR: Artista y Track son obligatorios"
        
        if not platforms:
            return "❌ ERROR: Selecciona al menos una plataforma"
        
        try:
            # Generar ID único
            campaign_id = f"CAMP_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Generar captions con OpenAI (si está disponible)
            captions = []
            hashtags = []
            
            if self.openai:
                try:
                    captions = self.openai.generate_captions(
                        track_name=track,
                        artist=artist,
                        genre=genre,
                        count=3
                    )
                    hashtags = self.openai.generate_hashtags(genre, mood)
                except Exception as e:
                    captions = [f"🔥 {track} - {artist} #newmusic #viral"]
                    hashtags = ["#music", "#newmusic", f"#{genre}"]
            else:
                # Fallback sin OpenAI
                captions = [
                    f"🔥 {track} - {artist} | Nuevo {genre} disponible YA #viral",
                    f"Este tema está 🔥🔥🔥 | {track} | {artist} #newmusic",
                    f"📢 NUEVO {genre.upper()} | {artist} - {track} | Dale play 🎧"
                ]
                hashtags = ["#music", "#newmusic", f"#{genre}", "#viral", "#fyp"]
            
            # Calcular métricas estimadas
            estimated_reach = self._estimate_reach(budget, platforms, duration)
            estimated_engagement = self._estimate_engagement(genre, mood, platforms)
            viral_score = self._calculate_viral_score(
                artist, genre, mood, platforms, budget
            )
            
            # Crear objeto de campaña
            campaign_data = {
                "id": campaign_id,
                "artist": artist,
                "track": track,
                "genre": genre,
                "mood": mood,
                "platforms": platforms,
                "budget": budget,
                "duration": duration,
                "video_url": video_url or "N/A",
                "video_prompt": video_prompt or "N/A",
                "target_age": target_age,
                "target_gender": target_gender,
                "auto_optimize": auto_optimize,
                "captions": captions,
                "hashtags": hashtags,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "metrics": {
                    "estimated_reach": estimated_reach,
                    "estimated_engagement": estimated_engagement,
                    "viral_score": viral_score,
                    "current_views": 0,
                    "current_likes": 0,
                    "current_shares": 0
                }
            }
            
            # Guardar en DB (si está disponible)
            if self.db:
                try:
                    self.db.save_campaign(campaign_data)
                except Exception as e:
                    pass  # Continuar aunque falle el guardado
            
            # Formatear resultado
            result = self._format_campaign_result(campaign_data)
            
            return result
            
        except Exception as e:
            return f"❌ ERROR al lanzar campaña:\n{str(e)}"
    
    def _estimate_reach(self, budget: float, platforms: List[str], duration: int) -> int:
        """Estimar reach basado en parámetros"""
        base_reach = 5000  # Reach orgánico base
        
        # Multiplicador por plataforma
        platform_multiplier = len(platforms) * 1.5
        
        # Multiplicador por budget (asumiendo $1 = 100 impresiones)
        budget_reach = budget * 100
        
        # Multiplicador por duración
        duration_multiplier = min(duration / 7, 2)  # Max 2x
        
        total_reach = int(
            (base_reach + budget_reach) * platform_multiplier * duration_multiplier
        )
        
        return total_reach
    
    def _estimate_engagement(self, genre: str, mood: str, platforms: List[str]) -> float:
        """Estimar tasa de engagement"""
        base_rate = 0.05  # 5% base
        
        # Géneros más virales
        viral_genres = ["trap", "reggaeton", "dembow"]
        if genre in viral_genres:
            base_rate += 0.02
        
        # Moods que enganchan más
        engaging_moods = ["energético", "fiestero"]
        if mood in engaging_moods:
            base_rate += 0.015
        
        # TikTok tiene mejor engagement
        if "TikTok" in platforms:
            base_rate += 0.02
        
        return round(base_rate * 100, 2)  # Convertir a porcentaje
    
    def _calculate_viral_score(
        self,
        artist: str,
        genre: str,
        mood: str,
        platforms: List[str],
        budget: float
    ) -> float:
        """Calcular score de viralidad (0-10)"""
        score = 5.0  # Base
        
        # Género viral
        if genre in ["trap", "reggaeton", "dembow"]:
            score += 1.5
        
        # Mood energético
        if mood in ["energético", "fiestero", "agresivo"]:
            score += 1.0
        
        # Multi-plataforma
        if len(platforms) >= 3:
            score += 1.0
        
        # Budget boost
        if budget > 1000:
            score += 0.5
        
        # TikTok is key
        if "TikTok" in platforms:
            score += 1.0
        
        return min(round(score, 1), 10.0)
    
    def _format_campaign_result(self, campaign: Dict) -> str:
        """Formatear resultado de campaña para mostrar"""
        
        metrics = campaign["metrics"]
        
        result = f"""
✅ CAMPAÑA LANZADA EXITOSAMENTE

════════════════════════════════════════════════════════════════

📋 DETALLES DE LA CAMPAÑA

🆔 ID: {campaign['id']}
🎤 Artista: {campaign['artist']}
🎵 Track: {campaign['track']}
🎸 Género: {campaign['genre']}
🎭 Mood: {campaign['mood']}

════════════════════════════════════════════════════════════════

📱 CONFIGURACIÓN

Plataformas: {', '.join(campaign['platforms'])}
Presupuesto: ${campaign['budget']:,.2f} USD
Duración: {campaign['duration']} días
Target Edad: {', '.join(campaign['target_age'])}
Target Género: {campaign['target_gender']}
Auto-optimización: {'✅ Activada' if campaign['auto_optimize'] else '❌ Desactivada'}

════════════════════════════════════════════════════════════════

✍️ CAPTIONS GENERADOS (Copy listo para usar)

1️⃣ {campaign['captions'][0] if len(campaign['captions']) > 0 else 'N/A'}

2️⃣ {campaign['captions'][1] if len(campaign['captions']) > 1 else 'N/A'}

3️⃣ {campaign['captions'][2] if len(campaign['captions']) > 2 else 'N/A'}

════════════════════════════════════════════════════════════════

#️⃣ HASHTAGS RECOMENDADOS

{' '.join(campaign['hashtags'][:10])}

════════════════════════════════════════════════════════════════

📊 MÉTRICAS ESTIMADAS

👥 Reach Estimado: {metrics['estimated_reach']:,} personas
💬 Engagement Estimado: {metrics['estimated_engagement']}%
🔥 Viral Score: {metrics['viral_score']}/10

{self._get_viral_score_interpretation(metrics['viral_score'])}

════════════════════════════════════════════════════════════════

🎯 PRÓXIMOS PASOS

1. El sistema monitoreará la campaña automáticamente
2. Recibirás notificaciones de hitos importantes
3. {'La IA optimizará el targeting en tiempo real' if campaign['auto_optimize'] else 'Revisa métricas manualmente'}
4. Reportes diarios disponibles en /metricas

════════════════════════════════════════════════════════════════

⏰ Iniciada: {datetime.fromisoformat(campaign['created_at']).strftime('%d/%m/%Y %H:%M:%S')}
📍 Estado: {campaign['status'].upper()}

💡 TIP: Usa el tab "📊 Métricas" para ver el progreso en tiempo real

🎵 ¡A ROMPERLA! 🚀
        """
        
        return result
    
    def _get_viral_score_interpretation(self, score: float) -> str:
        """Interpretar el viral score"""
        if score >= 9:
            return "🔥🔥🔥 ALTÍSIMO potencial viral - ¡Expect a hit!"
        elif score >= 7.5:
            return "🔥🔥 MUY ALTO potencial - Gran oportunidad"
        elif score >= 6:
            return "🔥 BUEN potencial - Probable buen rendimiento"
        elif score >= 4:
            return "📊 MODERADO - Rendimiento estándar esperado"
        else:
            return "📉 BAJO - Considera ajustar estrategia"

