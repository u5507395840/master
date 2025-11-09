import os
from flask import Flask, request, jsonify
from openai import OpenAI

# Importar módulos del sistema
try:
    from campaign_manager.manager import CampaignManager
    from analytics.dashboard import AnalyticsDashboard
    from ml_engine.models import MLEngine
    from uploaders.youtube_client import YouTubeClient
    from uploaders.meta_client import MetaClient
    from compliance.checks import ComplianceChecker
    
    campaign_mgr = CampaignManager()
    analytics = AnalyticsDashboard()
    ml_engine = MLEngine()
    youtube = YouTubeClient()
    meta = MetaClient()
    compliance = ComplianceChecker()
    
    MODULES_LOADED = True
except ImportError as e:
    print(f"⚠️  Módulos en placeholder mode: {e}")
    MODULES_LOADED = False

app = Flask(__name__)

# Cliente OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/health', methods=['GET'])
def health():
    """Health check del sistema completo"""
    status = {
        "status": "healthy",
        "service": "Discográfica ML Pro",
        "version": "2.0",
        "modules": {
            "chatbot_openai": bool(os.getenv('OPENAI_API_KEY')),
            "campaign_manager": MODULES_LOADED,
            "analytics": MODULES_LOADED,
            "ml_engine": MODULES_LOADED,
            "youtube_api": MODULES_LOADED,
            "meta_ads_api": MODULES_LOADED,
            "compliance": MODULES_LOADED
        }
    }
    return jsonify(status), 200

@app.route('/', methods=['GET'])
def index():
    """Página principal"""
    return jsonify({
        "service": "Discográfica ML Pro - AI System",
        "version": "2.0",
        "description": "Sistema completo de gestión discográfica con IA",
        "openai_enabled": bool(os.getenv('OPENAI_API_KEY')),
        "endpoints": {
            "/": "Esta página",
            "/health": "Health check completo",
            "/chat": "Chatbot OpenAI (GET/POST)",
            "/campaigns": "Gestión de campañas (GET/POST)",
            "/analytics": "Dashboard de analytics",
            "/upload/youtube": "Subir a YouTube (POST)",
            "/upload/meta": "Publicar en Meta Ads (POST)",
            "/ml/predict": "Predicciones ML (POST)",
            "/compliance/check": "Verificación compliance (POST)"
        }
    }), 200

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    """Chatbot con OpenAI"""
    try:
        if request.method == 'GET':
            message = request.args.get('message', '')
        else:
            data = request.get_json()
            message = data.get('message', '')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({"error": "OpenAI API key not configured"}), 503
        
        # Contexto del sistema
        system_context = f"""
        Eres el asistente IA de Discográfica ML Pro, un sistema completo de gestión discográfica.
        
        Estado de módulos: {"Activos" if MODULES_LOADED else "En desarrollo"}
        
        Puedes ayudar con:
        - Gestión de campañas de marketing musical
        - Analytics y métricas de rendimiento
        - Predicciones con Machine Learning
        - Distribución en YouTube
        - Publicidad en Meta Ads (Facebook/Instagram)
        - Verificación de compliance y derechos de autor
        
        Responde de forma profesional, útil y enfocada en la industria musical.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_context},
                {"role": "user", "content": message}
            ],
            max_tokens=300
        )
        
        reply = response.choices[0].message.content
        
        return jsonify({
            "message": message,
            "reply": reply,
            "model": "gpt-3.5-turbo",
            "system": "Discográfica ML Pro",
            "modules_active": MODULES_LOADED
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/campaigns', methods=['GET', 'POST'])
def campaigns():
    """Gestión de campañas"""
    if not MODULES_LOADED:
        return jsonify({"error": "Módulos no disponibles"}), 503
    
    if request.method == 'GET':
        result = campaign_mgr.list_campaigns()
        return jsonify(result), 200
    else:
        data = request.get_json() or {}
        result = campaign_mgr.create_campaign(data)
        return jsonify(result), 201

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Dashboard de analytics"""
    if not MODULES_LOADED:
        return jsonify({"error": "Módulos no disponibles"}), 503
    
    data = analytics.get_dashboard_data()
    return jsonify(data), 200

@app.route('/upload/youtube', methods=['POST'])
def upload_youtube():
    """Subir contenido a YouTube"""
    if not MODULES_LOADED:
        return jsonify({"error": "Módulos no disponibles"}), 503
    
    data = request.get_json() or {}
    result = youtube.upload_video(data)
    return jsonify(result), 200

@app.route('/upload/meta', methods=['POST'])
def upload_meta():
    """Publicar en Meta Ads"""
    if not MODULES_LOADED:
        return jsonify({"error": "Módulos no disponibles"}), 503
    
    data = request.get_json() or {}
    result = meta.create_ad(data)
    return jsonify(result), 200

@app.route('/ml/predict', methods=['POST'])
def ml_predict():
    """Predicciones con ML"""
    if not MODULES_LOADED:
        return jsonify({"error": "Módulos no disponibles"}), 503
    
    data = request.get_json() or {}
    prediction = ml_engine.predict(data)
    return jsonify({"prediction": prediction}), 200

@app.route('/compliance/check', methods=['POST'])
def compliance_check():
    """Verificación de compliance"""
    if not MODULES_LOADED:
        return jsonify({"error": "Módulos no disponibles"}), 503
    
    data = request.get_json() or {}
    result = compliance.check_content(data)
    return jsonify(result), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
