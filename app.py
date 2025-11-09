"""
🎵 DISCOGRÁFICA ML SYSTEM - API REST PRINCIPAL
Flask API + OpenAI + Video Generation
"""
import os
import logging
from flask import Flask, request, jsonify
from openai import OpenAI
from openai_orchestrator import get_orchestrator
from video_generator import VideoGenerator
from campaign_automator import CampaignLauncher

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Instancias globales
def get_openai_client():
    """Return OpenAI client if API key is set"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set")
        return None
    return OpenAI(api_key=api_key)

orchestrator = get_orchestrator()
video_gen = VideoGenerator()
campaign_launcher = CampaignLauncher()


@app.route('/')
def home():
    """Homepage con info del sistema"""
    return jsonify({
        "name": "Discográfica ML System",
        "version": "2.0.0",
        "description": "Sistema de automatización musical con IA",
        "features": [
            "OpenAI Strategy Generation",
            "Automatic Video Creation",
            "Multi-platform Campaign Launch",
            "Real-time Analytics",
            "Community Management"
        ],
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)",
            "strategy": "/api/strategy (POST)",
            "video": "/api/video/generate (POST)",
            "campaign": "/api/campaign/launch (POST)"
        },
        "dashboards": {
            "production_controller": "http://localhost:7860",
            "analytics_engine": "http://localhost:8501"
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "openai": "configured" if os.getenv('OPENAI_API_KEY') else "not configured",
        "timestamp": "2024-11-09T12:00:00Z"
    })


@app.route('/chat', methods=['POST'])
def chat():
    """Chatbot con OpenAI"""
    client = get_openai_client()
    if not client:
        return jsonify({"error": "OPENAI_API_KEY not configured"}), 503
    
    data = request.get_json() or {}
    message = data.get("message", "")
    
    if not message:
        return jsonify({"error": "message required"}), 400
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en marketing musical y campañas virales."},
                {"role": "user", "content": message}
            ]
        )
        
        return jsonify({
            "response": response.choices[0].message.content,
            "model": "gpt-4o-mini"
        })
    
    except Exception as e:
        logger.error(f"Error en chat: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/strategy', methods=['POST'])
def generate_strategy():
    """Genera estrategia de campaña con IA"""
    data = request.get_json() or {}
    
    track_info = {
        "artist": data.get("artist", "Unknown"),
        "title": data.get("title", "Unknown"),
        "genre": data.get("genre", "Unknown"),
        "description": data.get("description", ""),
        "budget": data.get("budget", 500)
    }
    
    try:
        strategy = orchestrator.generate_campaign_strategy(track_info)
        return jsonify({
            "status": "success",
            "strategy": strategy
        })
    
    except Exception as e:
        logger.error(f"Error generando estrategia: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/generate', methods=['POST'])
def generate_video_endpoint():
    """Endpoint para generar videos"""
    # TODO: Implementar upload de archivos
    return jsonify({
        "status": "pending",
        "message": "Video generation endpoint - en desarrollo"
    })


@app.route('/api/campaign/launch', methods=['POST'])
def launch_campaign_endpoint():
    """Endpoint para lanzar campañas"""
    data = request.get_json() or {}
    
    track_info = {
        "artist": data.get("artist"),
        "title": data.get("title"),
        "genre": data.get("genre"),
        "budget": data.get("budget", 500)
    }
    
    try:
        # Generar estrategia
        strategy = orchestrator.generate_campaign_strategy(track_info)
        
        # Lanzar campaña
        result = campaign_launcher.launch(
            track_info=track_info,
            strategy=strategy,
            video_path=data.get("video_path")
        )
        
        return jsonify({
            "status": "success",
            "campaign": result
        })
    
    except Exception as e:
        logger.error(f"Error lanzando campaña: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
