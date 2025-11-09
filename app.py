"""
Discográfica ML System - API Principal
Sistema completo de automatización musical con IA
"""
import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
import psutil

# Importar módulos del sistema
try:
    from integrations.meta.ads_manager import meta_ads_manager
    from integrations.youtube.uploader import youtube_uploader
    from integrations.tiktok.engagement_bot import tiktok_bot
    from ml_engine.metrics_analyzer import metrics_analyzer
    from ml_engine.vision.yolo_analyzer import yolo_analyzer
except ImportError as e:
    logging.warning(f"Some modules not available: {e}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuración
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DUMMY_MODE = os.getenv("DUMMY_MODE", "true").lower() == "true"

@app.route('/')
def index():
    """Endpoint principal"""
    return jsonify({
        "service": "Stakazo Discográfica ML System",
        "version": "2.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "mode": "dummy" if DUMMY_MODE else "production",
        "endpoints": {
            "health": "/health",
            "system_info": "/api/system/info",
            
            # Campaign Management
            "launch_campaign": "/api/campaign/launch",
            "campaign_metrics": "/api/campaign/metrics/<campaign_id>",
            
            # Meta Ads
            "create_meta_campaign": "/api/meta/campaign",
            "meta_metrics": "/api/meta/metrics/<campaign_id>",
            
            # YouTube
            "upload_youtube": "/api/youtube/upload",
            "youtube_analytics": "/api/youtube/analytics/<video_id>",
            
            # TikTok
            "tiktok_engage": "/api/tiktok/engage",
            "tiktok_trends": "/api/tiktok/trends",
            
            # ML & Analytics
            "viral_score": "/api/ml/viral-score",
            "predict_reach": "/api/ml/predict-reach",
            "analyze_video": "/api/ml/analyze-video",
            
            # Dashboards
            "production_controller": "http://localhost:7860",
            "analytics_engine": "http://localhost:8501"
        }
    })

@app.route('/health')
def health():
    """Health check"""
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory().percent
        
        healthy = cpu < 95 and memory < 95
        
        return jsonify({
            "status": "healthy" if healthy else "degraded",
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": cpu,
            "memory_percent": memory,
            "openai_configured": bool(OPENAI_API_KEY),
            "mode": "dummy" if DUMMY_MODE else "production"
        }), 200 if healthy else 503
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

@app.route('/api/campaign/launch', methods=['POST'])
def launch_campaign():
    """Lanzar campaña viral completa"""
    try:
        data = request.get_json()
        
        artist = data.get('artist', 'Unknown Artist')
        track = data.get('track', 'Unknown Track')
        video_prompt = data.get('video_prompt', '')
        platforms = data.get('platforms', ['TikTok', 'Instagram'])
        
        result = {
            "status": "success",
            "campaign_id": f"camp_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "artist": artist,
            "track": track,
            "platforms": platforms,
            "video_generated": bool(video_prompt),
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Campaign launch error: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/api/meta/campaign', methods=['POST'])
def create_meta_campaign():
    """Crear campaña en Meta Ads"""
    try:
        data = request.get_json()
        result = meta_ads_manager.create_campaign(
            name=data.get('name', 'Campaign'),
            objective=data.get('objective', 'VIDEO_VIEWS'),
            budget=data.get('budget', 50)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/meta/metrics/<campaign_id>')
def meta_metrics(campaign_id):
    """Obtener métricas de Meta Ads"""
    try:
        metrics = meta_ads_manager.get_campaign_metrics(campaign_id)
        return jsonify(metrics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/youtube/upload', methods=['POST'])
def upload_youtube():
    """Subir video a YouTube"""
    try:
        data = request.get_json()
        result = youtube_uploader.upload_video(
            video_path=data.get('video_path', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            tags=data.get('tags', [])
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tiktok/engage', methods=['POST'])
def tiktok_engage():
    """Engagement automático en TikTok"""
    try:
        data = request.get_json()
        result = tiktok_bot.auto_engage(
            hashtags=data.get('hashtags', []),
            limit=data.get('limit', 50)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tiktok/trends')
def tiktok_trends():
    """Obtener trends de TikTok"""
    try:
        trends = tiktok_bot.get_trending_sounds()
        return jsonify({"trends": trends})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ml/viral-score', methods=['POST'])
def viral_score():
    """Calcular score viral"""
    try:
        data = request.get_json()
        score = metrics_analyzer.calculate_viral_score(data)
        return jsonify({"viral_score": score})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ml/predict-reach', methods=['POST'])
def predict_reach():
    """Predecir reach futuro"""
    try:
        data = request.get_json()
        prediction = metrics_analyzer.predict_reach(data)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ml/analyze-video', methods=['POST'])
def analyze_video():
    """Analizar video con YOLO v8"""
    try:
        data = request.get_json()
        analysis = yolo_analyzer.analyze_video(data.get('video_path', ''))
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    logger.info(f"Starting Discográfica ML System on port {port}")
    logger.info(f"Mode: {'DUMMY' if DUMMY_MODE else 'PRODUCTION'}")
    app.run(host='0.0.0.0', port=port, debug=False)
