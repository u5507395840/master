#!/usr/bin/env python3
"""
DOGMA 24/7 - Meta Ads & YouTube Analytics API
"""
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'service': 'DOGMA 24/7',
        'version': '1.0.0',
        'status': 'running',
        'features': [
            'Meta Ads API',
            'YouTube Data API',
            'YouTube Analytics API'
        ]
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/meta/status')
def meta_status():
    return jsonify({
        'service': 'Meta Ads API',
        'configured': bool(os.getenv('META_ACCESS_TOKEN'))
    })

@app.route('/api/youtube/status')
def youtube_status():
    return jsonify({
        'service': 'YouTube API',
        'configured': bool(os.getenv('YOUTUBE_CLIENT_ID'))
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
