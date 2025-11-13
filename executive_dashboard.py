# Agregar al inicio de executive_dashboard.py
cat > fix-backend-url.py << 'EOF'
import sys

with open('executive_dashboard.py', 'r') as f:
    content = f.read()

# Agregar import os si no existe
if 'import os' not in content:
    content = 'import os\n' + content

# Reemplazar URL hardcodeada con variable de entorno
content = content.replace(
    'BACKEND_URL = os.getenv("BACKEND_URL", os.getenv("BACKEND_URL", os.getenv("BACKEND_URL", "http://localhost:8000")))',
    'BACKEND_URL = os.getenv("BACKEND_URL", os.getenv("BACKEND_URL", os.getenv("BACKEND_URL", "http://localhost:8000")))'
)

with open('executive_dashboard.py', 'w') as f:
    f.write(content)

print("✅ Backend URL actualizado")
EOF

python3 fix-backend-url.py
rm fix-backend-url.py
git add executive_dashboard.py
git commit -m "fix: use BACKEND_URL env variable"
git push
import os
# =======================
# IMPORTS Y VARIABLES GLOBALES
# =======================
import streamlit as st
import requests
import time
API_URL = "https://<tu-subdominio-railway>.railway.app"


# =======================
# IMPORTS Y VARIABLES GLOBALES
# =======================
import streamlit as st
import requests
import time
API_URL = "https://saliva-production.up.railway.app"


# --- Playground de Prompts IA (Profesional) ---
# --- Subida y validación de creativos ---
st.header("🎬 Subida y validación de creativos")
with st.form("creative_upload_form"):
    artist = st.text_input("Artista", "")
    genre = st.text_input("Género musical", "")
    subgenres = st.text_input("Subgéneros (separados por coma)", "")
    collaborators = st.text_input("Colaboradores (separados por coma)", "")
    language = st.text_input("Idioma", "es")
    notes = st.text_area("Notas adicionales", "")
    creative_file = st.file_uploader("Sube el archivo creativo (video, imagen, texto)")
    submitted = st.form_submit_button("Subir creativo y metadatos")
    if submitted and creative_file:
        import requests
        files = {"file": creative_file}
        data = {
            "artist": artist,
            "genre": genre,
            "subgenres": subgenres,
            "collaborators": collaborators,
            "language": language,
            "notes": notes
        }
        resp = requests.post(f"{API_URL}/upload_creative", data=data, files=files, verify=False)
        if resp.status_code == 200:
            st.success("Creativo y metadatos subidos correctamente.")
            result = resp.json()
            st.json(result.get("metadata", result))
        else:
            st.error(f"Error al subir creativo: {resp.text}")
st.sidebar.header("⚡ Separación de poderes IA")
st.sidebar.markdown("""
**Árbol ideográfico de modelos IA:**

Sistema Ejecutivo ML Musical
│
├── 1. Conversacional & Bot Telegram (GPT-3.5)
│     ├─ Playground de prompts IA (dashboard)
│     ├─ Chat ejecutivo y respuestas rápidas
│     ├─ Priorización y registro de acciones automáticas
│     └─ Bot Telegram: Listener, Executor, Interacción Emocional, Expansión Automática
│
├── 2. Control ML, Estrategia & Analíticas (GPT-5)
│     ├─ Orquestador central ML (backend)
│     ├─ Generación de estrategias avanzadas y prompts creativos
│     ├─ Automatización de campañas, triggers y publicación en satélites
│     ├─ Análisis de rendimiento, ROI y KPIs
│     └─ Decisiones de alto nivel y distribución de presupuesto
│
└── 3. Integración y Gobierno
    ├─ Dashboard: visualización, control y feedback
    ├─ Endpoints backend: reciben modelo a usar según el flujo
    └─ Separación clara: eficiencia conversacional (GPT-3.5) vs. profundidad analítica/estratégica (GPT-5)
""")

# Permitir al usuario seleccionar el modelo IA para cada flujo
st.sidebar.subheader("Selecciona el modelo IA para cada flujo")
model_playground = st.sidebar.selectbox("Modelo para Playground Conversacional", ["gpt-3.5-turbo", "gpt-5"], index=0)
model_strategy = st.sidebar.selectbox("Modelo para Estrategia/Analíticas", ["gpt-5", "gpt-3.5-turbo"], index=0)
st.header("📝 Playground de Prompts IA (Profesional)")

# Campo para la API Key de OpenAI
openai_api_key = st.text_input("Introduce tu API Key de OpenAI", type="password", key="openai_api_key")

prompt_playground = st.text_area("Escribe tu prompt personalizado para la IA", "", key="prompt_playground")
system_prompt_playground = st.text_area("Prompt de sistema (opcional)", "Eres un experto en marketing musical y automatización.", key="system_playground")
is_serious = st.checkbox("Marcar como prompt serio/productivo", value=False, key="serious_playground")

if "playground_history" not in st.session_state:
    st.session_state["playground_history"] = []

if st.button("Enviar prompt personalizado", key="btn_playground") and prompt_playground.strip():
    try:
        payload = {
            "prompt": prompt_playground,
            "system_prompt": system_prompt_playground,
            "history": st.session_state["playground_history"],
            "action": "serious" if is_serious else "playground",
            "openai_api_key": openai_api_key,
            "model": model_playground if not is_serious else model_strategy
        }
        endpoint = f"{API_URL}/openai_chat" if not is_serious else f"{API_URL}/ia_generate_strategy"
        resp = requests.post(endpoint, json=payload)
        playground_response = resp.json().get("response", resp.json().get("strategy", "[Sin respuesta]"))
        st.session_state["playground_history"].append({"role": "user", "content": prompt_playground})
        st.session_state["playground_history"].append({"role": "assistant", "content": playground_response})
        st.markdown("**Respuesta de la IA:**")
        st.code(playground_response)
    except Exception as e:
        st.error(f"Error al enviar el prompt: {e}")

if st.session_state["playground_history"]:
    st.markdown("### Historial de Prompts IA")
    for msg in st.session_state["playground_history"]:
        if msg["role"] == "user":
            st.markdown(f"**Tú:** {msg['content']}")
        else:
            st.markdown(f"**IA:** {msg['content']}")

if "playground_history" not in st.session_state:
    st.session_state["playground_history"] = []

if st.button("Enviar prompt personalizado") and prompt_playground.strip():
    try:
        payload = {
            "prompt": prompt_playground,
            "system_prompt": system_prompt_playground,
            "history": st.session_state["playground_history"],
            "action": "serious" if is_serious else "playground"
        }
        # Si es serio, puedes enviar a un endpoint productivo (ejemplo)
        endpoint = f"{API_URL}/openai_chat" if not is_serious else f"{API_URL}/ia_generate_strategy"
        resp = requests.post(endpoint, json=payload)
        playground_response = resp.json().get("response", resp.json().get("strategy", "[Sin respuesta]"))
        st.session_state["playground_history"].append({"role": "user", "content": prompt_playground})
        st.session_state["playground_history"].append({"role": "assistant", "content": playground_response})
        st.markdown("**Respuesta de la IA:**")
        st.code(playground_response)
    except Exception as e:
        st.error(f"Error al enviar el prompt: {e}")

if st.session_state["playground_history"]:
    st.markdown("### Historial de Prompts IA")
    for msg in st.session_state["playground_history"]:
        if msg["role"] == "user":
            st.markdown(f"**Tú:** {msg['content']}")
        else:
            st.markdown(f"**IA:** {msg['content']}")

import streamlit as st
import requests
import time
API_URL = os.getenv("BACKEND_URL", os.getenv("BACKEND_URL", "http://localhost:8000"))
# --- Estrategia IA argumental avanzada ---
st.header("🧠 Estrategia IA argumental avanzada")
with st.form("ia_strategy_advanced_form"):
    st.markdown("Genera una estrategia argumental y prompts creativos para campañas musicales usando IA avanzada.")
    total_budget = st.number_input("Presupuesto total (€)", min_value=10.0, value=100.0, key="budget_advanced")
    youtube_channel_url = st.text_input("URL del canal de YouTube", key="yt_url_advanced")
    creativity_level = st.selectbox("Nivel de creatividad", ["bajo", "medio", "alto"], index=2, key="creativity_advanced")
    performance_data = {
        "views": st.number_input("Vistas", min_value=0, value=10000, key="views_advanced"),
        "clicks": st.number_input("Clics", min_value=0, value=500, key="clicks_advanced"),
        "cost": st.number_input("Coste (€)", min_value=0.0, value=50.0, key="cost_advanced")
    }
    submitted = st.form_submit_button("Generar estrategia IA avanzada")
    if submitted:
        try:
            resp = requests.post(f"{API_URL}/ia_generate_strategy", json={
                "performance_data": performance_data,
                "total_budget": total_budget,
                "youtube_channel_url": youtube_channel_url,
                "creativity_level": creativity_level
            }, verify=False)
            strategy = resp.json().get("strategy", "[Sin respuesta]")
            st.markdown("**Estrategia argumental generada por IA:**")
            if isinstance(strategy, dict):
                st.json(strategy)
            else:
                st.code(strategy)
        except Exception as e:
            st.error(f"Error al generar estrategia IA: {e}")

# --- Automatización publicación en satélites ---
st.header("🚀 Automatización publicación en cuentas satélite")
with st.form("auto_satellite_form"):
    api_keys = st.text_area("API Keys de cuentas satélite (una por línea)", key="api_sat_auto").splitlines()
    channel_id = st.text_input("ID del canal principal", key="channel_sat_auto")
    video_file_path = st.text_input("Ruta al archivo de video (.mp4)", key="file_sat_auto")
    submitted = st.form_submit_button("Automatizar publicación")
    if submitted:
        try:
            resp = requests.post(f"{API_URL}/direct_satellite_campaign", json={
                "api_keys": api_keys,
                "channel_id": channel_id,
                "video_metadata": {},  # Se genera automáticamente por la IA
                "video_file_path": video_file_path
            }, verify=False)
            result = resp.json().get("result", [])
            if not result:
                st.error("No se obtuvo respuesta del backend.")
            else:
                for idx, res in enumerate(result):
                    if res.get("status") == "ok":
                        st.success(f"Cuenta {idx+1}: Video publicado correctamente (ID: {res.get('videoId')})")
                        st.markdown("**Análisis del video (dummy):**")
                        st.write(res.get("analysis", "dummy_analysis"))
                        st.markdown("**Prompt generado por IA (dummy):**")
                        st.code(res.get("prompt", "dummy_prompt"))
                        st.markdown("**Metadatos generados por IA (dummy):**")
                        st.json(res.get("metadatos", {}))
                    else:
                        st.error(f"Cuenta {idx+1}: Error al publicar - {res.get('error')}")
        except Exception as e:
            st.error(f"Error de conexión o backend: {e}")

# --- Visualización avanzada y feedback ---
st.header("📊 Visualización y feedback de campañas")
st.markdown("Visualización avanzada de resultados y KPIs. (En desarrollo)")
try:
    report = requests.get(f"{API_URL}/performance_report", params={"days": 30}, verify=False).json()
    st.subheader("Informe de rendimiento simulado")
    st.json(report)
    # Placeholder para gráficas y KPIs
    st.info("Próximamente: gráficas de rendimiento, KPIs y control granular de campañas.")
except Exception as e:
    st.warning(f"No se pudo obtener el informe: {e}")
# --- Estrategia y prompts creativos IA ---
st.header("🧠 Estrategia y prompts creativos IA")
with st.form("ia_strategy_form"):
    st.markdown("Genera una estrategia argumental y prompts creativos para campañas musicales usando IA.")
    total_budget = st.number_input("Presupuesto total (€)", min_value=10.0, value=100.0)
    youtube_channel_url = st.text_input("URL del canal de YouTube")
    creativity_level = st.selectbox(
        "Nivel de creatividad",
        ["bajo", "medio", "alto", "máximo"],
        index=2
    )
    # Simula datos de rendimiento (puedes conectar con el backend real)
    performance_data = {
        "views": st.number_input("Vistas", min_value=0, value=10000),
        "clicks": st.number_input("Clics", min_value=0, value=500),
        "cost": st.number_input("Coste (€)", min_value=0.0, value=50.0)
    }
    submitted = st.form_submit_button("Generar estrategia IA")
    if submitted:
        try:
            resp = requests.post(f"{API_URL}/ia_generate_strategy", json={
                "performance_data": performance_data,
                "total_budget": total_budget,
                "youtube_channel_url": youtube_channel_url,
                "creativity_level": creativity_level
            }, verify=False)
            strategy = resp.json().get("strategy", "[Sin respuesta]")
            st.markdown("**Estrategia argumental generada por IA:**")
            if isinstance(strategy, dict):
                st.json(strategy)
            else:
                st.code(strategy)
        except Exception as e:
            st.error(f"Error al generar estrategia IA: {e}")
# --- Campaña directa en cuentas satélite YouTube ---
st.header("🎯 Campaña 1 a 1 en cuentas satélite YouTube")
with st.form("direct_satellite_form"):
    api_keys = st.text_area("API Keys de cuentas satélite (una por línea)").splitlines()
    channel_id = st.text_input("ID del canal principal")
    video_title = st.text_input("Título del video")
    video_description = st.text_area("Descripción del video")
    video_tags = st.text_input("Tags (separados por coma)")
    video_file_path = st.text_input("Ruta al archivo de video (.mp4)")
    submitted = st.form_submit_button("Lanzar campaña directa")
    if submitted:
        video_metadata = {
            "title": video_title,
            "description": video_description,
            "tags": [t.strip() for t in video_tags.split(",") if t.strip()]
        }
        try:
            resp = requests.post(f"{API_URL}/direct_satellite_campaign", json={
                "api_keys": api_keys,
                "channel_id": channel_id,
                "video_metadata": video_metadata,
                "video_file_path": video_file_path
            }, verify=False)
            result = resp.json().get("result", [])
            if not result:
                st.error("No se obtuvo respuesta del backend.")
            else:
                for idx, res in enumerate(result):
                    if res.get("status") == "ok":
                        st.success(f"Cuenta {idx+1}: Video publicado correctamente (ID: {res.get('videoId')})")
                        st.markdown("**Análisis del video (dummy):**")
                        st.write(res.get("analysis", "dummy_analysis"))
                        st.markdown("**Prompt generado por IA (dummy):**")
                        st.code(res.get("prompt", "dummy_prompt"))
                        st.markdown("**Metadatos generados por IA (dummy):**")
                        st.json(res.get("metadatos", {}))
                    else:
                        st.error(f"Cuenta {idx+1}: Error al publicar - {res.get('error')}")
        except Exception as e:
            st.error(f"Error de conexión o backend: {e}")
"""
Executive Dashboard - Panel de control total para Discográfica ML System
"""
import streamlit as st
import requests
import time

API_URL = os.getenv("BACKEND_URL", os.getenv("BACKEND_URL", "http://localhost:8000"))

st.set_page_config(page_title="Executive Dashboard ML", page_icon="🎛️", layout="wide")
st.title("🎛️ Panel Ejecutivo - Discográfica ML System")
st.markdown("Gobierna campañas, IA, Meta Ads, usuarios y más desde un solo lugar.")

# --- Estado del sistema ---
st.header("🟢 Estado del Sistema")
try:
    status = requests.get(f"{API_URL}/status").json()
    st.success(f"Orquestador: {status['orchestrator']}")
except Exception as e:
    st.error(f"No se pudo conectar al backend: {e}")

# --- OpenAI API Key ---
st.sidebar.header("🔑 OpenAI API Key")
api_key_input = st.sidebar.text_input("Introduce tu OpenAI API Key", type="password")
if st.sidebar.button("Validar y guardar API Key"):
    resp = requests.post(f"{API_URL}/set_openai_key", json={"api_key": api_key_input}, verify=False)
    if resp.json().get("valid"):
        st.sidebar.success("API Key válida y guardada.")
        st.session_state["chat_history"] = []  # Recargar el chat al cambiar la API Key
        time.sleep(1)
        st.experimental_rerun()  # Refresca la página tras validar la API Key
    else:
        st.sidebar.error(f"API Key inválida: {resp.json().get('status')}")
try:
    api_key_status = requests.get(f"{API_URL}/get_openai_key_status", verify=False).json()["status"]
    if api_key_status == "valid":
        st.sidebar.info("Estado de la API Key: ✅ Válida")
    elif api_key_status == "not set":
        st.sidebar.warning("Estado de la API Key: No configurada")
    elif "Incorrect API key provided" in api_key_status:
        st.sidebar.error("API Key inválida: Verifica que la key esté bien copiada, sin espacios ni saltos de línea. Puedes generar una nueva en https://platform.openai.com/account/api-keys.")
    elif "deactivated" in api_key_status or "expired" in api_key_status:
        st.sidebar.error("API Key desactivada o expirada: Revisa el estado en tu panel de OpenAI y genera una nueva si es necesario.")
    elif "network" in api_key_status or "connection" in api_key_status:
        st.sidebar.error("Error de red: El backend no puede conectar con OpenAI. Verifica tu conexión a internet y que no haya bloqueos de firewall.")
    else:
        st.sidebar.error(f"Estado de la API Key: {api_key_status}")
except Exception as e:
    st.sidebar.error(f"No se pudo consultar el estado de la API Key: {e}")

# --- Chat con OpenAI ---
st.header("🤖 Chat con OpenAI (Asistente IA)")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

user_input = st.text_area("Escribe tu pregunta o instrucción para la IA", "", key="user_input")
if st.button("Enviar a OpenAI") and user_input.strip():
    try:
        resp = requests.post(f"{API_URL}/openai_chat", json={
            "prompt": user_input,
            "history": st.session_state["chat_history"]
        }, verify=False)
        ai_response = resp.json().get("response", "[Sin respuesta]")
    except Exception as e:
        ai_response = f"[Error de conexión]: {e}"
    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    st.session_state["chat_history"].append({"role": "assistant", "content": ai_response})

for msg in st.session_state["chat_history"]:
    if msg["role"] == "user":
        st.markdown(f"**Tú:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")

# --- Meta Ads ---
st.header("💰 Control Meta Ads & ROI")
try:
    meta_status = requests.get(f"{API_URL}/meta_ads_status", verify=False).json()
    if meta_status["all_ok"]:
        st.success("Meta Ads: ✅ Configuración OK")
    else:
        st.error("Meta Ads: ❌ Faltan tokens/configuración")
        st.write(meta_status)
except Exception as e:
    st.error(f"No se pudo consultar Meta Ads: {e}")

st.subheader("Simular cálculo de ROI Meta Ads")
with st.form("roi_form"):
    spend_eur = st.number_input("Gasto (€)", min_value=0.0, value=100.0)
    revenue_eur = st.number_input("Ingresos (€)", min_value=0.0, value=150.0)
    clicks = st.number_input("Clicks", min_value=0, value=500)
    conversions = st.number_input("Conversiones", min_value=0, value=50)
    impressions = st.number_input("Impresiones", min_value=0, value=10000)
    submitted = st.form_submit_button("Calcular ROI")
    if submitted:
        try:
            roi_result = requests.post(f"{API_URL}/calculate_roi", json={
                "spend_eur": spend_eur,
                "revenue_eur": revenue_eur,
                "clicks": clicks,
                "conversions": conversions,
                "impressions": impressions
            }, verify=False).json()
            st.success("Resultados ROI Meta Ads:")
            st.json(roi_result)
        except Exception as e:
            st.error(f"No se pudo calcular el ROI: {e}")

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
        try:
            resp = requests.post(f"{API_URL}/launch_campaign", json={
                "track_name": track_name,
                "artist": artist,
                "video_prompt": video_prompt,
                "platforms": platforms,
                "budget_eur": budget_eur,
                "audience": audience,
                "hashtags": [h.strip() for h in hashtags.split(",") if h.strip()]
            }, verify=False)
            st.success(f"Resultado: {resp.json().get('msg')}")
        except Exception as e:
            st.error(f"No se pudo lanzar la campaña: {e}")

# --- Informe de rendimiento ---
st.header("📊 Informe de Rendimiento")
performance_days = st.slider("Días de rendimiento analizado", min_value=7, max_value=90, value=30)
if st.button("Ver informe simulado"):
    try:
        report = requests.get(f"{API_URL}/performance_report", params={"days": performance_days}, verify=False).json()
        st.subheader("Informe de rendimiento simulado")
        st.json(report)
    except Exception as e:
        st.error(f"No se pudo obtener el informe: {e}")

st.markdown("---")
st.caption("Desarrollado por @u5507395840 | Executive Dashboard para automatización musical ML.")
