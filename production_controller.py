"""
🎮 PRODUCTION CONTROLLER - DASHBOARD DE CONTROL DE CAMPAÑAS
Puerto 7860 - Gradio Interface
"""
import os
import gradio as gr
import json
from datetime import datetime
from pathlib import Path
from openai_orchestrator import get_orchestrator
from video_generator import VideoGenerator
from campaign_automator.launcher import CampaignLauncher

# Directorios
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Instancias globales
orchestrator = get_orchestrator()
video_gen = VideoGenerator()
campaign_launcher = CampaignLauncher()


def launch_viral_campaign(
    artist_name: str,
    track_title: str,
    genre: str,
    audio_file,
    cover_image,
    description: str,
    budget: float,
    video_style: str
):
    """🚀 BOTÓN ROJO - Lanza campaña viral completa"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Preparar info del track
        track_info = {
            "artist": artist_name,
            "title": track_title,
            "genre": genre,
            "description": description,
            "budget": budget,
            "timestamp": timestamp
        }
        
        status_updates = []
        status_updates.append("🎵 Iniciando campaña viral...")
        
        # 2. Generar estrategia con OpenAI
        status_updates.append("🤖 Generando estrategia con IA...")
        strategy = orchestrator.generate_campaign_strategy(track_info)
        
        # 3. Generar video
        if audio_file and cover_image:
            status_updates.append("🎬 Generando video automático...")
            
            audio_path = f"data/audio_{timestamp}.mp3"
            cover_path = f"data/cover_{timestamp}.jpg"
            
            # Guardar archivos
            with open(audio_path, 'wb') as f:
                f.write(audio_file)
            with open(cover_path, 'wb') as f:
                f.write(cover_image)
            
            # Generar video
            video_path = video_gen.create_cover_video(
                audio_path,
                cover_path,
                track_title,
                artist_name,
                f"video_{timestamp}.mp4"
            )
            
            status_updates.append(f"✅ Video creado: {video_path}")
        else:
            status_updates.append("⚠️ Sin audio/cover - usando estrategia sin video")
            video_path = None
        
        # 4. Lanzar campaña en plataformas
        status_updates.append("📱 Publicando en redes sociales...")
        
        campaign_result = campaign_launcher.launch(
            track_info=track_info,
            strategy=strategy,
            video_path=video_path
        )
        
        status_updates.append("✅ Campaña lanzada en todas las plataformas!")
        
        # 5. Generar resumen
        summary = f"""
# 🚀 CAMPAÑA VIRAL LANZADA

## 📊 Información
- **Artista:** {artist_name}
- **Track:** {track_title}
- **Género:** {genre}
- **Presupuesto:** ${budget}

## 🎯 Estrategia Generada
- **Plataformas:** {', '.join(strategy.get('platforms', []))}
- **Hashtags:** {' '.join(strategy.get('hashtags', [])[:5])}
- **Mejor momento:** {strategy.get('posting_schedule', {}).get('day')} a las {strategy.get('posting_schedule', {}).get('time')}

## 📈 Resultados Esperados
- **Alcance estimado:** {campaign_result.get('estimated_reach', 'N/A')}
- **Engagement esperado:** {campaign_result.get('estimated_engagement', 'N/A')}

## 🎬 Assets Generados
- Video: {'✅ Creado' if video_path else '❌ No disponible'}
- Caption: {strategy.get('caption', 'N/A')[:100]}...

---
**Timestamp:** {timestamp}
**Campaign ID:** {campaign_result.get('campaign_id', 'N/A')}
"""
        
        return "\n".join(status_updates), summary, json.dumps(strategy, indent=2)
        
    except Exception as e:
        error_msg = f"❌ ERROR: {str(e)}"
        return error_msg, error_msg, "{}"


def generate_video_only(
    track_title: str,
    artist_name: str,
    audio_file,
    cover_image,
    video_type: str
):
    """Genera solo video sin lanzar campaña"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not audio_file or not cover_image:
            return "❌ Se requiere audio y cover image", None
        
        # Guardar archivos
        audio_path = f"data/audio_{timestamp}.mp3"
        cover_path = f"data/cover_{timestamp}.jpg"
        
        with open(audio_path, 'wb') as f:
            f.write(audio_file)
        with open(cover_path, 'wb') as f:
            f.write(cover_image)
        
        # Generar video según tipo
        if video_type == "Cover Video":
            video_path = video_gen.create_cover_video(
                audio_path, cover_path, track_title, artist_name
            )
        elif video_type == "Visualizer":
            video_path = video_gen.create_visualizer_video(
                audio_path, track_title, artist_name
            )
        else:
            return "❌ Tipo de video no soportado", None
        
        return f"✅ Video generado: {video_path}", video_path
        
    except Exception as e:
        return f"❌ Error: {str(e)}", None


def get_ai_recommendation(genre: str, target: str, budget: float):
    """Obtiene recomendación de IA para la campaña"""
    try:
        track_info = {
            "genre": genre,
            "target_audience": target,
            "budget": budget
        }
        
        strategy = orchestrator.generate_campaign_strategy(track_info)
        
        recommendation = f"""
# 🤖 RECOMENDACIÓN DE IA

## 📱 Plataformas Prioritarias
{', '.join(strategy.get('platforms', []))}

## 🎯 Estrategia de Contenido
{strategy.get('engagement_strategy', ['Estrategia no disponible'])[0]}

## 💰 Distribución de Presupuesto
"""
        for platform, allocation in strategy.get('budget_allocation', {}).items():
            recommendation += f"\n- **{platform}:** ${budget * allocation:.2f} ({allocation*100:.0f}%)"
        
        recommendation += f"""

## �� Target Audience
{strategy.get('target_audience', 'Gen Z, música urbana')}

## #️⃣ Hashtags Recomendados
{' '.join(strategy.get('hashtags', [])[:8])}
"""
        
        return recommendation
        
    except Exception as e:
        return f"❌ Error obteniendo recomendación: {str(e)}"


# Crear interfaz Gradio
with gr.Blocks(title="🎵 Discográfica ML - Production Controller", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # 🎵 DISCOGRÁFICA ML - PRODUCTION CONTROLLER
    ## 🚀 Sistema de Automatización Musical con IA
    
    **Controla tus campañas virales desde un solo lugar**
    """)
    
    with gr.Tabs():
        
        # TAB 1: LANZAR CAMPAÑA VIRAL
        with gr.Tab("🚀 Lanzar Campaña Viral"):
            gr.Markdown("### 🔴 BOTÓN ROJO - Campaña Automática Completa")
            
            with gr.Row():
                with gr.Column():
                    artist_input = gr.Textbox(label="👤 Artista", placeholder="Nombre del artista")
                    title_input = gr.Textbox(label="🎵 Título del Track", placeholder="Título de la canción")
                    genre_input = gr.Dropdown(
                        label="🎸 Género",
                        choices=["Trap", "Reggaeton", "Hip Hop", "Pop", "R&B", "Electronic", "Rock"],
                        value="Trap"
                    )
                    description_input = gr.Textbox(
                        label="📝 Descripción",
                        placeholder="Describe el track, mood, mensaje...",
                        lines=3
                    )
                    budget_input = gr.Slider(
                        label="💰 Presupuesto ($)",
                        minimum=50,
                        maximum=5000,
                        value=500,
                        step=50
                    )
                    video_style_input = gr.Dropdown(
                        label="🎬 Estilo de Video",
                        choices=["viral", "cinematic", "urban", "neon", "minimal"],
                        value="viral"
                    )
                
                with gr.Column():
                    audio_input = gr.File(label="🎵 Audio del Track (MP3)", file_types=[".mp3", ".wav"])
                    cover_input = gr.File(label="🖼️ Cover Image (JPG/PNG)", file_types=[".jpg", ".png"])
            
            launch_btn = gr.Button("🚀 LANZAR CAMPAÑA VIRAL", variant="primary", size="lg")
            
            with gr.Row():
                status_output = gr.Textbox(label="📊 Estado", lines=8)
                summary_output = gr.Markdown(label="📋 Resumen")
            
            strategy_output = gr.JSON(label="🤖 Estrategia Generada")
            
            launch_btn.click(
                fn=launch_viral_campaign,
                inputs=[
                    artist_input, title_input, genre_input,
                    audio_input, cover_input, description_input,
                    budget_input, video_style_input
                ],
                outputs=[status_output, summary_output, strategy_output]
            )
        
        # TAB 2: GENERAR VIDEO SOLO
        with gr.Tab("🎬 Generar Video"):
            gr.Markdown("### Genera video sin lanzar campaña")
            
            with gr.Row():
                with gr.Column():
                    video_title = gr.Textbox(label="Título")
                    video_artist = gr.Textbox(label="Artista")
                    video_audio = gr.File(label="Audio", file_types=[".mp3", ".wav"])
                    video_cover = gr.File(label="Cover Image", file_types=[".jpg", ".png"])
                    video_type = gr.Radio(
                        label="Tipo de Video",
                        choices=["Cover Video", "Visualizer", "Lyric Video"],
                        value="Cover Video"
                    )
                    gen_video_btn = gr.Button("🎬 Generar Video", variant="secondary")
                
                with gr.Column():
                    video_status = gr.Textbox(label="Estado", lines=5)
                    video_output = gr.File(label="Video Generado")
            
            gen_video_btn.click(
                fn=generate_video_only,
                inputs=[video_title, video_artist, video_audio, video_cover, video_type],
                outputs=[video_status, video_output]
            )
        
        # TAB 3: RECOMENDACIONES IA
        with gr.Tab("🤖 Recomendaciones IA"):
            gr.Markdown("### Obtén estrategia personalizada con OpenAI")
            
            with gr.Row():
                with gr.Column():
                    rec_genre = gr.Dropdown(
                        label="Género",
                        choices=["Trap", "Reggaeton", "Hip Hop", "Pop", "R&B"],
                        value="Trap"
                    )
                    rec_target = gr.Textbox(
                        label="Target Audience",
                        value="Gen Z, 16-24, urban music"
                    )
                    rec_budget = gr.Slider(
                        label="Presupuesto",
                        minimum=50,
                        maximum=5000,
                        value=500
                    )
                    rec_btn = gr.Button("🤖 Obtener Recomendación", variant="secondary")
                
                with gr.Column():
                    rec_output = gr.Markdown(label="Recomendación")
            
            rec_btn.click(
                fn=get_ai_recommendation,
                inputs=[rec_genre, rec_target, rec_budget],
                outputs=[rec_output]
            )
    
    gr.Markdown("""
    ---
    ### 📊 Métricas en Tiempo Real
    Accede al **Analytics Engine** en [http://localhost:8501](http://localhost:8501)
    
    🔥 **Sistema desarrollado con ❤️ para artistas independientes**
    """)


if __name__ == "__main__":
    print("🎮 Iniciando Production Controller...")
    print("🌐 Abriendo en: http://localhost:7860")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
