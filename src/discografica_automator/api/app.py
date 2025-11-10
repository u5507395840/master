import logging
from flask import Flask, jsonify, request
from threading import Thread

# Rutas de importación actualizadas
from discografica_automator.core.database import (
    get_all_campaigns, get_campaign_by_id, save_campaign, update_campaign_status
)
from discografica_automator.services import campaign_launcher

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"}), 200

@app.route('/api/campaigns', methods=['GET'])
def list_campaigns():
    campaigns = get_all_campaigns()
    return jsonify([campaign.to_dict() for campaign in campaigns])

@app.route('/api/campaign/create', methods=['POST'])
def create_campaign():
    data = request.get_json()
    if not data or 'artist' not in data or 'track' not in data:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    
    campaign = save_campaign(
        artist=data['artist'],
        track=data['track'],
        video_prompt=data.get('video_prompt', '')
    )
    return jsonify({"status": "success", "campaign": campaign.to_dict()}), 201

@app.route('/api/campaign/<campaign_id>/launch', methods=['POST'])
def launch_campaign_endpoint(campaign_id):
    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        return jsonify({"status": "error", "message": "Campaign not found"}), 404

    if campaign.status not in ["PENDING", "FAILED"]:
        return jsonify({"status": "error", "message": f"Campaign already {campaign.status}"}), 409

    # Lanzar en un hilo para no bloquear la respuesta de la API
    thread = Thread(target=campaign_launcher.launch_campaign, args=(campaign_id,))
    thread.start()
    
    update_campaign_status(campaign_id, "QUEUED")
    return jsonify({"status": "success", "message": f"Campaign {campaign_id} queued for launch."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
