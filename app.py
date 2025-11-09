"""
🎵 DISCOGRÁFICA ML SYSTEM - API REST INTEGRADA
═══════════════════════════════════════════════════════════
Merge: Esqueleto Flask base + Funcionalidades ML especializadas
═══════════════════════════════════════════════════════════
"""
import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from openai import OpenAI

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# IMPORTS NUEVOS (Módulos Discográfica ML)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
try:
    from openai_orchestrator import get_orchestrator
    ORCHESTRATOR_AVAILABLE = True
except ImportError:
    ORCHESTRATOR_AVAILABLE = False
    logging.warning("OpenAI Orchestrator no disponible - usando modo básico")

try:
    from video_generator import VideoGenerator
    VIDEO_GEN_AVAILABLE = True
except ImportError:
    VIDEO_GEN_AVAILABLE = False
    logging.warning("Video Generator no disponible")

try:
    from campaign_automator import CampaignLauncher
    CAMPAIGN_AVAILABLE = True
except ImportError:
    CAMPAIGN_AVAILABLE = False
    logging.warning("Campaign Automator no disponible")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURACIÓN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLIENTE OPENAI (Esqueleto base - CONSERVADO)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_openai_client():
    """Return OpenAI client if API key is set"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("⚠️  OPENAI_API_KEY not configured")
        return None
    return OpenAI(api_key=api_key)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INSTANCIAS GLOBALES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
orchestrator = get_orchestrator() if ORCHESTRATOR_AVAILABLE else None
video_gen = VideoGenerator() if VIDEO_GEN_AVAILABLE else None
campaign_launcher = CampaignLauncher() if CAMPAIGN_AVAILABLE else None


# ═══════════════════════════════════════════════════
# RUTAS BASE (Esqueleto - CONSERVADAS)
# ═══════════════════════════════════════════════════

@app.route('/')
def home():
    """Homepage con info del sistema integrado"""
    modules_status = {
        "openai_orchestrator": "✅ Disponible" if ORCHESTRATOR_AVAILABLE else "⚠️  No disponible",
        "video_generator": "✅ Disponible" if VIDEO_GEN_AVAILABLE else "⚠️  No disponible",
        "campaign_automator": "✅ Disponible" if CAMPAIGN_AVAILABLE else "⚠️  No disponible"
    }
    
    return jsonify({
        "name": "🎵 Discográfica ML System",
        "version": "2.0.0-integrated",
        "description": "Sistema integral de automatización musical con IA",
        "architecture": "Merge: Esqueleto Flask + Módulos ML especializados",
        "modules": modules_status,
        "features": [
            "OpenAI Chat (base)",
            "OpenAI Strategy Generation (ML)",
            "Automatic Video Creation (ML)",
            "Multi-platform Campaign Launch (ML)",
            "Real-time Analytics (ML)",
            "Community Management (ML)"
        ],
        "endpoints": {
            "base": {
                "health": "/health",
                "chat": "/chat (POST)"
            },
            "ml_features": {
                "strategy": "/api/strategy (POST)",
                "video": "/api/video/generate (POST)",
                "campaign": "/api/campaign/launch (POST)",
                "analyze": "/api/analytics/analyze (POST)"
            }
        },
        "dashboards": {
            "production_controller": "http://localhost:7860 (si disponible)",
            "analytics_engine": "http://localhost:8501 (si disponible)"
        },
        "timestamp": datetime.now().isoformat()
    })


@app.route('/health')
def health():
    """Health check endpoint (Esqueleto base - CONSERVADO)"""
    return jsonify({
        "status": "healthy",
        "openai": "configured" if os.getenv('OPENAI_API_KEY') else "not configured",
        "modules": {
            "orchestrator": ORCHESTRATOR_AVAILABLE,
            "video_generator": VIDEO_GEN_AVAILABLE,
            "campaign_automator": CAMPAIGN_AVAILABLE
        },
        "timestamp": datetime.now().isoformat()
    })


@app.route('/chat', methods=['POST'])
def chat():
    """Chatbot con OpenAI (Esqueleto base - CONSERVADO)"""
    client = get_openai_client()
    if not client:
        return jsonify({
            "error": "OPENAI_API_KEY not configured",
            "status": "service_unavailable"
        }), 503
    
    data = request.get_json() or {}
    message = data.get("message", "")
    
    if not message:
        return jsonify({"error": "message required"}), 400
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente experto en marketing musical y campañas virales para discográficas."
                },
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )
        
        return jsonify({
            "response": response.choices[0].message.content,
            "model": "gpt-4o-mini",
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error en chat: {e}")
        return jsonify({"error": str(e)}), 500


# ═══════════════════════════════════════════════════
# RUTAS ML (NUEVAS - Funcionalidad Discográfica ML)
# ═══════════════════════════════════════════════════

@app.route('/api/strategy', methods=['POST'])
def generate_strategy():
    """Genera estrategia de campaña con IA (NUEVO)"""
    if not ORCHESTRATOR_AVAILABLE:
        return jsonify({
            "error": "OpenAI Orchestrator no disponible",
            "fallback": "Usando estrategia básica"
        }), 503
    
    data = request.get_json() or {}
    
    track_info = {
        "artist": data.get("artist", "Unknown Artist"),
        "title": data.get("title", "Unknown Track"),
        "genre": data.get("genre", "Unknown"),
        "description": data.get("description", ""),
        "budget": data.get("budget", 500),
        "target_audience": data.get("target_audience", "Gen Z")
    }
    
    try:
        logger.info(f"🎯 Generando estrategia para: {track_info['title']}")
        strategy = orchestrator.generate_campaign_strategy(track_info)
        
        return jsonify({
            "status": "success",
            "track": track_info,
            "strategy": strategy,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error generando estrategia: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/video/prompt', methods=['POST'])
def generate_video_prompt():
    """Genera prompt para video con IA (NUEVO)"""
    if not ORCHESTRATOR_AVAILABLE:
        return jsonify({"error": "OpenAI Orchestrator no disponible"}), 503
    
    data = request.get_json() or {}
    
    track_info = {
        "genre": data.get("genre", "trap"),
        "mood": data.get("mood", "energetic"),
        "target_audience": data.get("target_audience", "Gen Z")
    }
    
    style = data.get("style", "viral")
    
    try:
        prompt = orchestrator.generate_video_prompt(track_info, style)
        
        return jsonify({
            "status": "success",
            "prompt": prompt,
            "style": style,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error generando prompt: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/campaign/launch', methods=['POST'])
def launch_campaign():
    """Lanza campaña completa (NUEVO)"""
    if not CAMPAIGN_AVAILABLE:
        return jsonify({"error": "Campaign Automator no disponible"}), 503
    
    data = request.get_json() or {}
    
    track_info = {
        "artist": data.get("artist", "Unknown"),
        "title": data.get("title", "Unknown"),
        "genre": data.get("genre", "Unknown"),
        "budget": data.get("budget", 500)
    }
    
    try:
        logger.info(f"🚀 Lanzando campaña: {track_info['title']}")
        
        # Generar estrategia si orchestrator disponible
        if ORCHESTRATOR_AVAILABLE:
            strategy = orchestrator.generate_campaign_strategy(track_info)
        else:
            strategy = {"platforms": ["TikTok", "Instagram"]}
        
        # Lanzar campaña
        result = campaign_launcher.launch(
            track_info=track_info,
            strategy=strategy,
            video_path=data.get("video_path")
        )
        
        return jsonify({
            "status": "success",
            "campaign": result,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error lanzando campaña: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analytics/analyze', methods=['POST'])
def analyze_metrics():
    """Analiza métricas con IA (NUEVO)"""
    if not ORCHESTRATOR_AVAILABLE:
        return jsonify({"error": "OpenAI Orchestrator no disponible"}), 503
    
    data = request.get_json() or {}
    metrics = data.get("metrics", {})
    
    try:
        logger.info("📊 Analizando métricas con IA...")
        analysis = orchestrator.analyze_metrics(metrics)
        
        return jsonify({
            "status": "success",
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error analizando métricas: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/community/respond', methods=['POST'])
def community_respond():
    """Genera respuesta para community management (NUEVO)"""
    if not ORCHESTRATOR_AVAILABLE:
        return jsonify({"error": "OpenAI Orchestrator no disponible"}), 503
    
    data = request.get_json() or {}
    comment = data.get("comment", "")
    context = data.get("context", "")
    
    if not comment:
        return jsonify({"error": "comment required"}), 400
    
    try:
        response = orchestrator.generate_community_response(comment, context)
        
        return jsonify({
            "status": "success",
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error generando respuesta: {e}")
        return jsonify({"error": str(e)}), 500


# ═══════════════════════════════════════════════════
# INFORMACIÓN DEL SISTEMA
# ═══════════════════════════════════════════════════

@app.route('/api/system/info')
def system_info():
    """Información completa del sistema integrado"""
    return jsonify({
        "system": "Discográfica ML System",
        "version": "2.0.0-integrated",
        "architecture": {
            "base": "Flask REST API con OpenAI",
            "extensions": [
                "OpenAI Orchestrator (estrategias IA)",
                "Video Generator (MoviePy)",
                "Campaign Automator (multi-plataforma)",
                "Analytics Engine (ML predictions)"
            ]
        },
        "modules_loaded": {
            "orchestrator": ORCHESTRATOR_AVAILABLE,
            "video_generator": VIDEO_GEN_AVAILABLE,
            "campaign_automator": CAMPAIGN_AVAILABLE
        },
        "capabilities": {
            "chat": True,
            "strategy_generation": ORCHESTRATOR_AVAILABLE,
            "video_generation": VIDEO_GEN_AVAILABLE,
            "campaign_launch": CAMPAIGN_AVAILABLE,
            "analytics": ORCHESTRATOR_AVAILABLE,
            "community_management": ORCHESTRATOR_AVAILABLE
        },
        "environment": {
            "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
            "port": int(os.getenv("PORT", 8080))
        }
    })


# ═══════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    
    logger.info("═══════════════════════════════════════════════")
    logger.info("🎵 DISCOGRÁFICA ML SYSTEM - INICIANDO")
    logger.info("═══════════════════════════════════════════════")
    logger.info(f"🌐 Puerto: {port}")
    logger.info(f"🤖 OpenAI: {'✅ Configurado' if os.getenv('OPENAI_API_KEY') else '⚠️  No configurado'}")
    logger.info(f"🎯 Orchestrator: {'✅' if ORCHESTRATOR_AVAILABLE else '❌'}")
    logger.info(f"🎬 Video Gen: {'✅' if VIDEO_GEN_AVAILABLE else '❌'}")
    logger.info(f"📱 Campaign: {'✅' if CAMPAIGN_AVAILABLE else '❌'}")
    logger.info("═══════════════════════════════════════════════")
    
    app.run(host='0.0.0.0', port=port, debug=False)
