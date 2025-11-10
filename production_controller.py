"""Production Controller - Dashboard REAL"""
import gradio as gr
import os
from datetime import datetime
from orchestrator_ml.copy_generator import copy_generator

campaigns_db = []

def launch_campaign(artist, track, genre, video_prompt, platforms):
    if not artist or not track:
        return "❌ Completa artista y track"
    captions = copy_generator.generate_captions(track, artist, genre or "trap", count=3)
    hashtags = copy_generator.generate_hashtags(genre or "trap")
    campaign = {"id": f"CAMP_{datetime.now().strftime('%Y%m%d%H%M%S')}", "artist": artist, 
                "track": track, "status": "active", "captions": captions, "hashtags": hashtags}
    campaigns_db.append(campaign)
    return f"✅ CAMPAÑA LANZADA\n\nID: {campaign['id']}\nArtista: {artist}\nTrack: {track}\n\n" \
           f"Captions:\n1. {captions[0]}\n2. {captions[1]}\n3. {captions[2]}\n\nHashtags: {' '.join(hashtags[:5])}"

def get_metrics():
    if not campaigns_db:
        return "📊 No hay campañas activas"
    return f"📊 MÉTRICAS\n\n🎯 Campañas: {len(campaigns_db)}\n⚡ Activas: {sum(1 for c in campaigns_db if c['status']=='active')}"

def generate_copy(track, artist, genre):
    if not track or not artist:
        return "⚠️ Completa track y artista"
    captions = copy_generator.generate_captions(track, artist, genre or "trap", count=5)
    hashtags = copy_generator.generate_hashtags(genre or "trap")
    return f"✅ COPY GENERADO\n\n🎵 {track} - {artist}\n\n" + "\n".join([f"{i+1}. {c}" for i,c in enumerate(captions)]) + \
           f"\n\n#️⃣ {' '.join(hashtags)}"

with gr.Blocks(title="Production Controller", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎵 PRODUCTION CONTROLLER")
    with gr.Tabs():
        with gr.Tab("🚀 Lanzar"):
            with gr.Row():
                with gr.Column():
                    artist = gr.Textbox(label="Artista")
                    track = gr.Textbox(label="Track")
                    genre = gr.Dropdown(["trap","reggaeton","rap"], label="Género", value="trap")
                    video = gr.Textbox(label="Video prompt (opcional)", lines=2)
                    platforms = gr.CheckboxGroup(["TikTok","Instagram","YouTube"], label="Plataformas", value=["TikTok"])
                    btn = gr.Button("🔴 LANZAR", variant="primary")
                with gr.Column():
                    output = gr.Textbox(label="Resultado", lines=20)
            btn.click(launch_campaign, [artist,track,genre,video,platforms], output)
        with gr.Tab("✍️ Copy"):
            with gr.Row():
                with gr.Column():
                    copy_track = gr.Textbox(label="Track")
                    copy_artist = gr.Textbox(label="Artista")
                    copy_genre = gr.Dropdown(["trap","reggaeton"], value="trap")
                    copy_btn = gr.Button("✨ Generar")
                with gr.Column():
                    copy_out = gr.Textbox(label="Copy", lines=25)
            copy_btn.click(generate_copy, [copy_track,copy_artist,copy_genre], copy_out)
        with gr.Tab("📊 Métricas"):
            metrics_out = gr.Textbox(label="Métricas", lines=20)
            gr.Button("🔄 Actualizar").click(get_metrics, outputs=metrics_out)
    gr.Markdown("💜 Stakazo System")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("GRADIO_PORT", 7860)), share=False)
