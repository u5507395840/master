#!/bin/bash
echo "🧠 Starting ML Engine..."
uvicorn analytics_engine:app --host 0.0.0.0 --port ${PORT:-8001}
