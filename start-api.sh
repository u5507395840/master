#!/bin/bash
echo "🚀 Starting DOGMA API..."
uvicorn executive_api:app --host 0.0.0.0 --port ${PORT:-8000}
