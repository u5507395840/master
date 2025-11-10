"""Flask API - Sistema REAL"""
import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
import psutil
try:
    from orchestrator_ml.copy_generator import copy_generator
except:
    copy_generator = None

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
campaigns_db = []

@app.route('/')
def index():
    return jsonify({"service": "Stakazo System", "version": "2.0-REAL", "status": "operational",
                    "endpoints": {"/health": "Health check", "/api/copy/generate": "Generate copy",
                                 "/api/campaign/launch": "Launch campaign", "/api/metrics": "Get metrics"}})

@app.route('/health')
def health():
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory().percent
    return jsonify({"status": "healthy" if cpu<90 else "degraded", "cpu": cpu, "memory": mem,
                    "openai": bool(os.getenv("OPENAI_API_KEY"))}), 200 if cpu<90 else 503

@app.route('/api/copy/generate', methods=['POST'])
def gen_copy():
    data = request.get_json()
    if not copy_generator or not data.get('track') or not data.get('artist'):
        return jsonify({"error": "Missing data"}), 400
    captions = copy_generator.generate_captions(data['track'], data['artist'], data.get('genre','trap'))
    return jsonify({"status": "success", "captions": captions})

@app.route('/api/campaign/launch', methods=['POST'])
def launch():
    data = request.get_json()
    campaign = {"id": f"CAMP_{datetime.now().strftime('%Y%m%d%H%M%S')}", "artist": data.get('artist'),
                "track": data.get('track'), "status": "active", "created": datetime.now().isoformat()}
    campaigns_db.append(campaign)
    return jsonify({"status": "success", "campaign": campaign})

@app.route('/api/metrics')
def metrics():
    return jsonify({"total": len(campaigns_db), "active": sum(1 for c in campaigns_db if c['status']=='active')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)), debug=False)
