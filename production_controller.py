"""
Production Controller - Dashboard Gradio para control de campañas
"""
import gradio as gr
import os
import json
from datetime import datetime
import requests

# Configuración
API_BASE = os.getenv("API_BASE", "http://localhost:8080")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ProductionController:
    def __init__(self):
        self.campaign_status = "idle"
        self.last_launch = None
    
    def launch_viral_campaign(self, artist_name, track_name, video_prompt, platforms):
        """Lanzar campaña viral completa"""
        
        self.campaign_status = "launching"
        self.last_launch = datetime.now()
        
        result = {
            "status": "success",
            "timestamp": self.last_launch.isoformat(),
            "artist": artist_name,
            "track": track_name,
            "platforms": platforms,
            "video_generated": False,
            "campaigns_created": []
        }
        
        # Simular generación de video
        if video_prompt:
            result["video_generated"] = True
            result["video_url"] = f"https://storage.example.com/videos/{track_name.lower().replace(' ', '_')}.mp4"
        
        # Simular creación de campañas
        for platform in platforms:
            campaign = {
                "platform": platform,
                "status": "active",
                "budget": 50 if platform == "Meta" else 0,
                "estimated_reach": 10000
            }
            result["campaigns_created"].append(campaign)
        
        self.campaign_status = "active"
        
        return json.dumps(result, indent=2)
    
    def get_campaign_metrics(self):
        """Obtener métricas de campañas activas"""
        
        if self.campaign_status == "idle":
            return "No hay campañas activas"
        
        metrics = {
            "status": self.campaign_status,
            "last_launch": self.last_launch.isoformat() if self.last_launch else None,
            "active_campaigns": 3,
            "total_reach": 45230,
            "engagement_rate": 8.5,
            "viral_score": 7.2,
            "platforms": {
                "TikTok": {"views": 25000, "likes": 2100, "shares": 450},
                "Instagram": {"views": 15000, "likes": 1280, "comments": 230},
                "YouTube": {"views": 5230, "likes": 420, "comments": 89}
            }
        }
        
        return json.dumps(metrics, indent=2)
    
    def stop_campaigns(self):
        """Detener todas las campañas"""
        self.campaign_status = "stopped"
        return "✅ Todas las campañas detenidas"

# Instancia global
controller = ProductionController()

# Interfaz Gradio
def create_interface():
    with gr.Blocks(title="🎵 Production Controller", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🎵 PRODUCTION CONTROLLER")
        gr.Markdown("### Control centralizado de campañas virales musicales")
        
        with gr.Tab("🚀 Lanzar Campaña"):
            with gr.Row():
                with gr.Column():
                    artist_input = gr.Textbox(label="Nombre del Artista", placeholder="Ej: Bad Bunny")
                    track_input = gr.Textbox(label="Nombre del Track", placeholder="Ej: Tití Me Preguntó")
                    video_prompt = gr.Textbox(
                        label="Prompt para Video IA", 
                        placeholder="Ej: Artista de trap en estudio con luces neón moradas",
                        lines=3
                    )
                    platforms = gr.CheckboxGroup(
                        ["TikTok", "Instagram", "YouTube", "Meta Ads"],
                        label="Plataformas",
                        value=["TikTok", "Instagram"]
                    )
                    
                    launch_btn = gr.Button("🔴 LANZAR CAMPAÑA VIRAL", variant="primary", size="lg")
                
                with gr.Column():
                    launch_output = gr.JSON(label="Resultado del Lanzamiento")
            
            launch_btn.click(
                fn=controller.launch_viral_campaign,
                inputs=[artist_input, track_input, video_prompt, platforms],
                outputs=launch_output
            )
        
        with gr.Tab("📊 Métricas en Vivo"):
            with gr.Row():
                metrics_output = gr.JSON(label="Métricas de Campañas Activas")
                refresh_btn = gr.Button("🔄 Actualizar Métricas")
            
            refresh_btn.click(
                fn=controller.get_campaign_metrics,
                outputs=metrics_output
            )
        
        with gr.Tab("⚙️ Control"):
            with gr.Column():
                gr.Markdown("### Controles de Sistema")
                stop_btn = gr.Button("🛑 Detener Todas las Campañas", variant="stop")
                stop_output = gr.Textbox(label="Estado")
            
            stop_btn.click(
                fn=controller.stop_campaigns,
                outputs=stop_output
            )
        
        gr.Markdown("---")
        gr.Markdown("💜 **Stakazo Discográfica ML System** | Powered by OpenAI o1")
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
