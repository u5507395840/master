import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Cliente OpenAI con variable de entorno (SEGURO)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        "status": "healthy",
        "service": "chatbot-ia",
        "openai_configured": bool(os.getenv('OPENAI_API_KEY'))
    }), 200

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    """Endpoint principal del chatbot"""
    try:
        # Obtener mensaje del query param o body
        if request.method == 'GET':
            message = request.args.get('message', '')
        else:
            data = request.get_json()
            message = data.get('message', '')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Llamar a OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente útil y amigable."},
                {"role": "user", "content": message}
            ],
            max_tokens=150
        )
        
        reply = response.choices[0].message.content
        
        return jsonify({
            "message": message,
            "reply": reply,
            "model": "gpt-3.5-turbo"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Página de inicio"""
    return jsonify({
        "service": "Chatbot IA",
        "version": "1.0",
        "endpoints": {
            "/health": "Health check",
            "/chat": "Chat endpoint (GET/POST)",
            "/": "This page"
        }
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
