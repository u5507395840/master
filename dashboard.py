"""
Dashboard AI para gobernar el orquestador y OpenAI
"""
import streamlit as st
import sys
import os
# Añadir el directorio 'src' al PYTHONPATH para encontrar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from discografica_automator.services.orchestrator import orchestrator
from analytics_engine import get_youtube_performance_report

st.set_page_config(page_title="AI Marketing Dashboard", page_icon="🤖", layout="wide")
st.title("🤖 Viral Marketing AI Dashboard")
st.markdown("Gobierna el sistema, lanza estrategias y consulta resultados.")

st.sidebar.header("⚙️ Parámetros de Estrategia")
total_budget = st.sidebar.number_input("Presupuesto total (EUR)", min_value=10.0, max_value=10000.0, value=100.0)
youtube_channel_url = st.sidebar.text_input("URL del canal de YouTube", value="https://www.youtube.com/channel/UC-ejd_S_a_i3c_d_s_e_g")
performance_days = st.sidebar.slider("Días de rendimiento analizado", min_value=7, max_value=90, value=30)

st.sidebar.header("🔑 Configuración de OpenAI API Key")
api_key_input = st.sidebar.text_input("Introduce tu OpenAI API Key", type="password")
if st.sidebar.button("Validar y guardar API Key"):
    if api_key_input:
        ok = orchestrator.set_api_key(api_key_input)
        if ok:
            st.sidebar.success("API Key válida y guardada.")
        else:
            st.sidebar.error(f"API Key inválida: {orchestrator.get_api_key_status()}")
    else:
        st.sidebar.warning("Introduce una API Key antes de validar.")

api_key_status = orchestrator.get_api_key_status()
if api_key_status == "valid":
    st.sidebar.info("Estado de la API Key: ✅ Válida")
elif api_key_status == "not set":
    st.sidebar.warning("Estado de la API Key: No configurada")
else:
    st.sidebar.error(f"Estado de la API Key: {api_key_status}")

st.sidebar.header("💰 Control Meta Ads & ROI")
meta_status = orchestrator.get_meta_ads_status()
if meta_status["all_ok"]:
    st.sidebar.success("Meta Ads: ✅ Configuración OK")
else:
    st.sidebar.error("Meta Ads: ❌ Faltan tokens/configuración")
    st.sidebar.write(meta_status)

st.sidebar.subheader("Simular cálculo de ROI Meta Ads")
spend_eur = st.sidebar.number_input("Gasto (€)", min_value=0.0, value=100.0)
revenue_eur = st.sidebar.number_input("Ingresos (€)", min_value=0.0, value=150.0)
clicks = st.sidebar.number_input("Clicks", min_value=0, value=500)
conversions = st.sidebar.number_input("Conversiones", min_value=0, value=50)
impressions = st.sidebar.number_input("Impresiones", min_value=0, value=10000)

if st.sidebar.button("Calcular ROI"):
    roi_result = orchestrator.calculate_roi({
        "spend_eur": spend_eur,
        "revenue_eur": revenue_eur,
        "clicks": clicks,
        "conversions": conversions,
        "impressions": impressions
    })
    st.sidebar.success("Resultados ROI Meta Ads:")
    st.sidebar.json(roi_result)

if st.sidebar.button("Generar Estrategia AI"):
    st.info("Solicitando estrategia a OpenAI...")
    performance_data = get_youtube_performance_report(days=performance_days)
    plan = orchestrator.decide_meta_ads_strategy(
        performance_data=performance_data,
        total_budget=total_budget,
        youtube_channel_url=youtube_channel_url
    )
    st.success("Estrategia generada:")
    for i, campaign in enumerate(plan["campaign_plan"]):
        st.write(f"**Satélite {i+1}:** {campaign['campaign_name']}")
        st.write(f"- Audiencia: {campaign['target_audience']}")
        st.write(f"- Prompt Creativo: {campaign['ad_creative_prompt']}")
        st.write(f"- Presupuesto: {campaign['budget_eur']} EUR")
        st.markdown("---")

st.sidebar.header("🔍 Consultar Informe de Rendimiento")
if st.sidebar.button("Ver informe simulado"):
    report = get_youtube_performance_report(days=performance_days)
    st.subheader("Informe de rendimiento simulado")
    st.json(report)

st.markdown("---")
st.caption("Desarrollado por @u5507395840 | Demo AI para automatización de campañas musicales.")
