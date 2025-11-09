"""
Analytics Engine - Dashboard Streamlit para análisis ML
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuración de página
st.set_page_config(
    page_title="Analytics Engine",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Analytics Engine")
st.markdown("### Análisis ML en Tiempo Real")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    time_range = st.selectbox("Rango de Tiempo", ["Últimas 24h", "Última semana", "Último mes"])
    platforms = st.multiselect("Plataformas", ["TikTok", "Instagram", "YouTube", "Meta Ads"], default=["TikTok", "Instagram"])
    
    st.markdown("---")
    st.metric("Campañas Activas", "3")
    st.metric("Total Invertido", "$150")

# Generar datos simulados
def generate_mock_data(days=7):
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    data = {
        'date': dates,
        'views': np.random.randint(5000, 25000, days),
        'likes': np.random.randint(400, 2100, days),
        'shares': np.random.randint(50, 450, days),
        'engagement_rate': np.random.uniform(5.0, 12.0, days)
    }
    return pd.DataFrame(data)

df = generate_mock_data()

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Views",
        f"{df['views'].sum():,}",
        f"+{df['views'].iloc[-1] - df['views'].iloc[-2]:,}"
    )

with col2:
    st.metric(
        "Total Engagement",
        f"{df['likes'].sum():,}",
        f"+{((df['likes'].iloc[-1] / df['likes'].iloc[-2] - 1) * 100):.1f}%"
    )

with col3:
    st.metric(
        "Avg Engagement Rate",
        f"{df['engagement_rate'].mean():.2f}%",
        f"+{(df['engagement_rate'].iloc[-1] - df['engagement_rate'].mean()):.2f}%"
    )

with col4:
    st.metric(
        "Viral Score",
        "7.2/10",
        "+0.8"
    )

st.markdown("---")

# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Views Over Time")
    fig_views = px.line(df, x='date', y='views', markers=True)
    fig_views.update_layout(height=300)
    st.plotly_chart(fig_views, use_container_width=True)

with col2:
    st.subheader("💚 Engagement Rate")
    fig_engagement = px.line(df, x='date', y='engagement_rate', markers=True)
    fig_engagement.update_layout(height=300)
    st.plotly_chart(fig_engagement, use_container_width=True)

# Análisis por plataforma
st.markdown("---")
st.subheader("📱 Análisis por Plataforma")

platform_data = pd.DataFrame({
    'Platform': ['TikTok', 'Instagram', 'YouTube'],
    'Views': [25000, 15000, 5230],
    'Engagement': [8.5, 7.2, 5.8],
    'Cost': [0, 0, 0]
})

col1, col2 = st.columns(2)

with col1:
    fig_platform = px.bar(platform_data, x='Platform', y='Views', color='Platform')
    st.plotly_chart(fig_platform, use_container_width=True)

with col2:
    fig_engagement_platform = px.pie(platform_data, values='Views', names='Platform')
    st.plotly_chart(fig_engagement_platform, use_container_width=True)

# Predicciones ML
st.markdown("---")
st.subheader("🤖 Predicciones ML")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Probabilidad Viral:** 72%")
    st.progress(0.72)

with col2:
    st.info("**Reach Estimado 24h:** 35,000")
    st.progress(0.65)

with col3:
    st.info("**ROI Proyectado:** 450%")
    st.progress(0.90)

# Footer
st.markdown("---")
st.markdown("💜 **Stakazo Discográfica ML System** | Powered by Ultralytics & OpenAI")

# Auto-refresh cada 30 segundos
st.markdown(
    """
    <script>
    setTimeout(function(){
        window.location.reload();
    }, 30000);
    </script>
    """,
    unsafe_allow_html=True
)
