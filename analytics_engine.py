"""
📊 ANALYTICS ENGINE - DASHBOARD DE MÉTRICAS Y ANÁLISIS
Puerto 8501 - Streamlit Interface
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from pathlib import Path
from openai_orchestrator import get_orchestrator

# Configuración de página
st.set_page_config(
    page_title="Discográfica ML - Analytics",
    page_icon="📊",
    layout="wide"
)

# Instancia del orchestrator
orchestrator = get_orchestrator()

# Título principal
st.title("📊 DISCOGRÁFICA ML - ANALYTICS ENGINE")
st.markdown("### 🎵 Análisis en Tiempo Real con IA")

# Sidebar
with st.sidebar:
    st.header("🎛️ Controles")
    
    time_range = st.selectbox(
        "📅 Rango de Tiempo",
        ["Últimas 24h", "Última semana", "Último mes", "Todo"]
    )
    
    platform_filter = st.multiselect(
        "📱 Plataformas",
        ["TikTok", "Instagram", "YouTube", "Facebook"],
        default=["TikTok", "Instagram"]
    )
    
    st.markdown("---")
    st.markdown("### 🤖 Análisis IA")
    
    if st.button("🔄 Actualizar Datos"):
        st.rerun()

# Métricas principales (KPIs)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👁️ Alcance Total",
        value="1.2M",
        delta="+15.3%"
    )

with col2:
    st.metric(
        label="💬 Engagement Rate",
        value="8.5%",
        delta="+2.1%"
    )

with col3:
    st.metric(
        label="🎵 Streams",
        value="450K",
        delta="+23%"
    )

with col4:
    st.metric(
        label="💰 ROI",
        value="3.2x",
        delta="+0.5x"
    )

# Gráficos
st.markdown("---")

# Row 1: Engagement por plataforma + Tendencia temporal
col1, col2 = st.columns(2)

with col1:
    st.subheader("📱 Engagement por Plataforma")
    
    # Datos dummy
    df_platform = pd.DataFrame({
        'Plataforma': ['TikTok', 'Instagram', 'YouTube', 'Facebook'],
        'Engagement': [12.5, 8.3, 5.2, 3.1],
        'Alcance': [800000, 450000, 320000, 180000]
    })
    
    fig = px.bar(
        df_platform,
        x='Plataforma',
        y='Engagement',
        color='Plataforma',
        title='Engagement Rate por Plataforma (%)'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📈 Tendencia de Alcance")
    
    # Datos dummy temporales
    dates = pd.date_range(start='2024-11-01', end='2024-11-09', freq='D')
    df_trend = pd.DataFrame({
        'Fecha': dates,
        'Alcance': [50000, 75000, 120000, 180000, 250000, 320000, 420000, 580000, 750000]
    })
    
    fig = px.line(
        df_trend,
        x='Fecha',
        y='Alcance',
        title='Evolución del Alcance (últimos 9 días)',
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

# Row 2: Top Tracks + Distribución de budget
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎵 Top Tracks")
    
    df_tracks = pd.DataFrame({
        'Track': ['Noche de Trap', 'Fuego', 'En la Calle', 'Vibras'],
        'Streams': [450000, 380000, 290000, 210000],
        'Engagement': [12.5, 10.2, 8.9, 7.1]
    })
    
    st.dataframe(
        df_tracks.style.background_gradient(subset=['Streams'], cmap='Blues'),
        use_container_width=True
    )

with col2:
    st.subheader("💰 Distribución de Presupuesto")
    
    df_budget = pd.DataFrame({
        'Plataforma': ['TikTok', 'Instagram', 'YouTube', 'Meta Ads'],
        'Inversión': [400, 350, 250, 300]
    })
    
    fig = px.pie(
        df_budget,
        values='Inversión',
        names='Plataforma',
        title='Distribución del Presupuesto ($)'
    )
    st.plotly_chart(fig, use_container_width=True)

# Análisis IA
st.markdown("---")
st.subheader("🤖 Análisis Inteligente con OpenAI")

col1, col2 = st.columns([2, 1])

with col1:
    # Métricas dummy para análisis
    dummy_metrics = {
        "total_reach": 1200000,
        "engagement_rate": 8.5,
        "roi": 3.2,
        "top_platform": "TikTok",
        "growth_rate": 15.3
    }
    
    if st.button("🔍 Generar Análisis IA", type="primary"):
        with st.spinner("Analizando datos con OpenAI..."):
            analysis = orchestrator.analyze_metrics(dummy_metrics)
            
            st.success("✅ Análisis completado")
            
            st.markdown(f"### 💡 Recomendación Principal")
            st.info(analysis.get('recommendation', 'No disponible'))
            
            st.markdown(f"### 🎯 Confianza: {analysis.get('confidence', 0)*100:.0f}%")
            
            if 'actions' in analysis:
                st.markdown("### 📋 Acciones Recomendadas")
                for i, action in enumerate(analysis['actions'], 1):
                    st.markdown(f"{i}. {action}")
            
            if 'opportunities' in analysis:
                st.markdown("### 🚀 Oportunidades Detectadas")
                for opp in analysis['opportunities']:
                    st.markdown(f"- {opp}")

with col2:
    st.markdown("### 📊 Métricas Clave")
    st.json(dummy_metrics)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🎵 <strong>Discográfica ML System</strong> | Desarrollado con ❤️ para artistas independientes</p>
    <p>🤖 Powered by OpenAI GPT-4 | 📊 Real-time Analytics</p>
</div>
""", unsafe_allow_html=True)
