"""
Supabase Connector - Gestión de reglas y triggers para aprendizaje continuo ML
"""
from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "<TU_SUPABASE_URL>")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "<TU_SUPABASE_KEY>")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_platform_rules(platform: str):
    response = supabase.table("platform_rules").select("*").eq("platform", platform).execute()
    return response.data

def insert_campaign_trigger(trigger_data: dict):
    response = supabase.table("campaign_triggers").insert(trigger_data).execute()
    return response.data

def get_campaign_triggers():
    response = supabase.table("campaign_triggers").select("*").execute()
    return response.data

# Ejemplo de uso:
if __name__ == "__main__":
    # Obtener reglas de YouTube
    yt_rules = get_platform_rules("youtube")
    print("Reglas YouTube:", yt_rules)
    # Insertar trigger de campaña
    trigger = {"platform": "youtube", "event": "deploy_satellite_shorts", "metrics": {"CTR": 1.3}}
    result = insert_campaign_trigger(trigger)
    print("Trigger insertado:", result)
    # Obtener triggers
    triggers = get_campaign_triggers()
    print("Triggers actuales:", triggers)
