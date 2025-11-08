#!/usr/bin/env python3
"""
DOGMA 24/7 - Meta Ads & YouTube Analytics API
Multi-platform marketing automation with AI
"""
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Service info endpoint"""
    return jsonify({
        'service': 'DOGMA 24/7',
        'version': '1.0.0',
        'status': 'running',
        'author': 'stakazo',
        'features': [
            'Meta Ads API',
            'YouTube Data API',
            'YouTube Analytics API',
            'OpenAI GPT-4 Integration'
        ]
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/meta/status')
def meta_status():
    """Check Meta Ads API configuration"""
    return jsonify({
        'service': 'Meta Ads API',
        'configured': bool(os.getenv('META_ACCESS_TOKEN'))
    })

@app.route('/api/youtube/status')
def youtube_status():
    """Check YouTube API configuration"""
    return jsonify({
        'service': 'YouTube API',
        'configured': bool(os.getenv('YOUTUBE_CLIENT_ID'))
    })

@app.route('/api/openai/status')
def openai_status():
    """Check OpenAI API configuration"""
    return jsonify({
        'service': 'OpenAI API',
        'configured': bool(os.getenv('OPENAI_API_KEY')),
        'model': os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
    })

@app.route('/api/ai/generate-ad-copy', methods=['POST'])
def generate_ad_copy_endpoint():
    """Generate ad copy with AI"""
    try:
        from openai_client import get_openai_client
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        client = get_openai_client()
        result = client.generate_ad_copy(
            product=data.get('product', ''),
            target_audience=data.get('target_audience', ''),
            tone=data.get('tone', 'profesional')
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
