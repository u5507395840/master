#!/bin/bash
echo "🎨 Starting DOGMA Dashboard..."
streamlit run executive_dashboard.py --server.port ${PORT:-8501} --server.address 0.0.0.0
