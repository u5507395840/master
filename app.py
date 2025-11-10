"""
Flask API - Sistema REAL con Database
"""
import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil

# Importar módulos propios
try:
    from orchestrator_ml.copy_generator import copy_generator
except ImportError:
    copy_generator = None

try:
    from core.database import db
except ImportError:
    db = None

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear app Flask
app = Flask(__name__)
CORS(app)

# ═══════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    """Endpoint raíz con información del sistema"""
    return jsonify({
        "service": "Stakazo Discográfica ML System",
        "version": "2.1-REAL",
        "status": "operational",
        "features": {
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "database": db is not None,
            "telegram": bool(os.getenv("TELEGRAM_BOT_TOKEN"))
        },
        "endpoints": {
            "GET /": "System info",
            "GET /health": "Health check",
            "POST /api/copy/generate": "Generate viral copy",
            "POST /api/campaign/launch": "Launch campaign",
            "GET /api/campaign/<id>": "Get campaign by ID",
            "GET /api/campaigns": "List all campaigns",
            "PATCH /api/campaign/<id>/status": "Update campaign status",
            "GET /api/metrics": "Get system metrics",
            "GET /api/stats": "Get database stats"
        }
    })

@app.route('/health')
def health():
    """Health check con métricas del sistema"""
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    status = "healthy"
    if cpu > 90 or mem.percent > 90:
        status = "degraded"
    
    response = {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "system": {
            "cpu_percent": cpu,
            "memory_percent": mem.percent,
            "memory_available_mb": mem.available // (1024 * 1024),
            "disk_percent": disk.percent
        },
        "services": {
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "database": db is not None,
            "telegram": bool(os.getenv("TELEGRAM_BOT_TOKEN"))
        }
    }
    
    status_code = 200 if status == "healthy" else 503
    return jsonify(response), status_code

@app.route('/api/copy/generate', methods=['POST'])
def generate_copy():
    """Generar copy viral con OpenAI"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if not data.get('track') or not data.get('artist'):
            return jsonify({"error": "Missing required fields: track, artist"}), 400
        
        # Generar copy
        if not copy_generator:
            return jsonify({"error": "OpenAI not configured"}), 503
        
        captions = copy_generator.generate_captions(
            track_name=data['track'],
            artist=data['artist'],
            genre=data.get('genre', 'trap'),
            platform=data.get('platform', 'tiktok'),
            count=data.get('count', 3)
        )
        
        hashtags = copy_generator.generate_hashtags(
            genre=data.get('genre', 'trap'),
            mood=data.get('mood', 'energetic')
        )
        
        # Log en database
        if db:
            db.log('INFO', 'api', 'Copy generated', {
                'track': data['track'],
                'artist': data['artist'],
                'captions_count': len(captions)
            })
        
        return jsonify({
            "status": "success",
            "data": {
                "captions": captions,
                "hashtags": hashtags,
                "track": data['track'],
                "artist": data['artist']
            }
        })
        
    except Exception as e:
        logger.error(f"Error generating copy: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/campaign/launch', methods=['POST'])
def launch_campaign():
    """Lanzar nueva campaña"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['artist', 'track']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Crear campaña
        campaign = {
            "id": f"CAMP_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "artist": data['artist'],
            "track": data['track'],
            "genre": data.get('genre', 'trap'),
            "mood": data.get('mood', 'energetic'),
            "platforms": data.get('platforms', ['TikTok']),
            "budget": data.get('budget', 0),
            "duration": data.get('duration', 7),
            "video_url": data.get('video_url'),
            "video_prompt": data.get('video_prompt'),
            "target_age": data.get('target_age', []),
            "target_gender": data.get('target_gender', 'Todos'),
            "auto_optimize": data.get('auto_optimize', True),
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "captions": [],
            "hashtags": [],
            "metrics": {
                "estimated_reach": 0,
                "estimated_engagement": 0,
                "viral_score": 0,
                "current_views": 0,
                "current_likes": 0,
                "current_shares": 0
            }
        }
        
        # Generar copy si OpenAI está disponible
        if copy_generator:
            try:
                campaign['captions'] = copy_generator.generate_captions(
                    campaign['track'],
                    campaign['artist'],
                    campaign['genre'],
                    count=3
                )
                campaign['hashtags'] = copy_generator.generate_hashtags(
                    campaign['genre'],
                    campaign['mood']
                )
            except:
                pass
        
        # Guardar en database
        if db:
            db.save_campaign(campaign)
            db.log('INFO', 'api', 'Campaign launched', {'campaign_id': campaign['id']})
        
        logger.info(f"Campaign launched: {campaign['id']}")
        
        return jsonify({
            "status": "success",
            "campaign": campaign
        }), 201
        
    except Exception as e:
        logger.error(f"Error launching campaign: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/campaign/<campaign_id>')
def get_campaign(campaign_id):
    """Obtener campaña por ID"""
    try:
        if not db:
            return jsonify({"error": "Database not available"}), 503
        
        campaign = db.get_campaign(campaign_id)
        
        if not campaign:
            return jsonify({"error": "Campaign not found"}), 404
        
        return jsonify({
            "status": "success",
            "campaign": campaign
        })
        
    except Exception as e:
        logger.error(f"Error getting campaign: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/campaigns')
def list_campaigns():
    """Listar todas las campañas"""
    try:
        if not db:
            return jsonify({"error": "Database not available"}), 503
        
        status_filter = request.args.get('status')
        campaigns = db.get_all_campaigns(status=status_filter)
        
        return jsonify({
            "status": "success",
            "count": len(campaigns),
            "campaigns": campaigns
        })
        
    except Exception as e:
        logger.error(f"Error listing campaigns: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/campaign/<campaign_id>/status', methods=['PATCH'])
def update_campaign_status(campaign_id):
    """Actualizar estado de campaña"""
    try:
        if not db:
            return jsonify({"error": "Database not available"}), 503
        
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['active', 'paused', 'completed', 'cancelled']:
            return jsonify({"error": "Invalid status"}), 400
        
        success = db.update_campaign_status(campaign_id, new_status)
        
        if not success:
            return jsonify({"error": "Failed to update campaign"}), 500
        
        db.log('INFO', 'api', 'Campaign status updated', {
            'campaign_id': campaign_id,
            'new_status': new_status
        })
        
        return jsonify({
            "status": "success",
            "campaign_id": campaign_id,
            "new_status": new_status
        })
        
    except Exception as e:
        logger.error(f"Error updating campaign: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/metrics')
def get_metrics():
    """Obtener métricas del sistema"""
    try:
        if not db:
            # Sin database, retornar métricas básicas
            return jsonify({
                "status": "success",
                "metrics": {
                    "total_campaigns": 0,
                    "active_campaigns": 0
                }
            })
        
        stats = db.get_stats()
        
        return jsonify({
            "status": "success",
            "metrics": stats
        })
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Obtener estadísticas de la base de datos"""
    try:
        if not db:
            return jsonify({"error": "Database not available"}), 503
        
        stats = db.get_stats()
        
        return jsonify({
            "status": "success",
            "stats": stats
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({"error": str(e)}), 500

# ═══════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    logger.info(f"🚀 Starting Stakazo API on port {port}")
    logger.info(f"📊 Database: {'✅ Connected' if db else '❌ Not available'}")
    logger.info(f"🤖 OpenAI: {'✅ Configured' if copy_generator else '❌ Not configured'}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

