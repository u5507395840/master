"""
Executive Dashboard - Panel de control total para Discográfica ML System
"""
import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Executive Dashboard ML", page_icon="🎛️", layout="wide")
st.title("🎛️ Panel Ejecutivo - Discográfica ML System")
st.markdown("Gobierna campañas, IA, Meta Ads, usuarios y más desde un solo lugar.")

# --- Estado del sistema ---
st.header("🟢 Estado del Sistema")
status = requests.get(f"{API_URL}/status").json()
st.success(f"Orquestador: {status['orchestrator']}")

# --- OpenAI API Key ---
st.sidebar.header("🔑 OpenAI API Key")
api_key_input = st.sidebar.text_input("Introduce tu OpenAI API Key", type="password")
if st.sidebar.button("Validar y guardar API Key"):
    resp = requests.post(f"{API_URL}/set_openai_key", json={"api_key": api_key_input})
    if resp.json().get("valid"):
        st.sidebar.success("API Key válida y guardada.")
    else:
        st.sidebar.error(f"API Key inválida: {resp.json().get('status')}")
api_key_status = requests.get(f"{API_URL}/get_openai_key_status").json()["status"]
if api_key_status == "valid":
    st.sidebar.info("Estado de la API Key: ✅ Válida")
elif api_key_status == "not set":
    st.sidebar.warning("Estado de la API Key: No configurada")
else:
    st.sidebar.error(f"Estado de la API Key: {api_key_status}")

# --- Meta Ads ---
st.header("💰 Control Meta Ads & ROI")
meta_status = requests.get(f"{API_URL}/meta_ads_status").json()
if meta_status["all_ok"]:
    st.success("Meta Ads: ✅ Configuración OK")
else:
    st.error("Meta Ads: ❌ Faltan tokens/configuración")
    st.write(meta_status)

st.subheader("Simular cálculo de ROI Meta Ads")
with st.form("roi_form"):
    spend_eur = st.number_input("Gasto (€)", min_value=0.0, value=100.0)
    revenue_eur = st.number_input("Ingresos (€)", min_value=0.0, value=150.0)
    clicks = st.number_input("Clicks", min_value=0, value=500)
    conversions = st.number_input("Conversiones", min_value=0, value=50)
    impressions = st.number_input("Impresiones", min_value=0, value=10000)
    submitted = st.form_submit_button("Calcular ROI")
    if submitted:
        roi_result = requests.post(f"{API_URL}/calculate_roi", json={
            "spend_eur": spend_eur,
            "revenue_eur": revenue_eur,
            "clicks": clicks,
            "conversions": conversions,
            "impressions": impressions
        }).json()
        st.success("Resultados ROI Meta Ads:")
        st.json(roi_result)

# --- Lanzar campaña ---
st.header("🚀 Lanzar Campaña Real")
with st.form("campaign_form"):
    track_name = st.text_input("Nombre del track")
    artist = st.text_input("Artista")
    video_prompt = st.text_area("Prompt para video")
    platforms = st.multiselect("Plataformas", ["TikTok", "Instagram", "YouTube", "Meta Ads"])
    budget_eur = st.number_input("Presupuesto (€)", min_value=10.0, value=100.0)
    audience = st.text_input("Audiencia objetivo (opcional)")
    hashtags = st.text_input("Hashtags (separados por coma)")
    submitted = st.form_submit_button("Lanzar campaña")
    if submitted:
        resp = requests.post(f"{API_URL}/launch_campaign", json={
            "track_name": track_name,
            "artist": artist,
            "video_prompt": video_prompt,
            "platforms": platforms,
            "budget_eur": budget_eur,
            "audience": audience,
            "hashtags": [h.strip() for h in hashtags.split(",") if h.strip()]
        })
        st.success(f"Resultado: {resp.json().get('msg')}")

# --- Informe de rendimiento ---
st.header("📊 Informe de Rendimiento")
performance_days = st.slider("Días de rendimiento analizado", min_value=7, max_value=90, value=30)
if st.button("Ver informe simulado"):
    report = requests.get(f"{API_URL}/performance_report", params={"days": performance_days}).json()
    st.subheader("Informe de rendimiento simulado")
    st.json(report)

# --- Chat con OpenAI (Asistente IA) ---
st.header("🤖 Chat con OpenAI (Asistente IA)")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

user_input = st.text_area("Escribe tu pregunta o instrucción para la IA", "", key="user_input")
if st.button("Enviar a OpenAI") and user_input.strip():
    # Llama al backend para obtener respuesta de OpenAI
    resp = requests.post(f"{API_URL}/openai_chat", json={"prompt": user_input, "history": st.session_state["chat_history"]})
    ai_response = resp.json().get("response", "[Sin respuesta]")
    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    st.session_state["chat_history"].append({"role": "assistant", "content": ai_response})

# Mostrar historial de chat
for msg in st.session_state["chat_history"]:
    if msg["role"] == "user":
        st.markdown(f"**Tú:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")

st.markdown("---")
st.caption("Desarrollado por @u5507395840 | Executive Dashboard para automatización musical ML.")
