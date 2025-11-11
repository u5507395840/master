"""
Supabase UTM Connector - Gestión de métricas UTM para ML y orquestación
"""
from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "<TU_SUPABASE_URL>")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "<TU_SUPABASE_KEY>")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_utm_metric(utm_data: dict):
    response = supabase.table("utm_metrics").insert(utm_data).execute()
    return response.data

def get_utm_metrics(filters: dict = None):
    query = supabase.table("utm_metrics").select("*")
    if filters:
        for k, v in filters.items():
            query = query.eq(k, v)
    response = query.execute()
    return response.data

# Ejemplo de uso:
if __name__ == "__main__":
    # Insertar métrica UTM
    utm = {
        "campaign": "spotify_launch_nov2025",
        "source": "instagram",
        "medium": "social",
        "term": "music",
        "content": "ad1",
        "clicks": 120,
        "conversions": 15,
        "timestamp": "2025-11-11T12:00:00Z"
    }
    result = insert_utm_metric(utm)
    print("UTM insertado:", result)
    # Consultar métricas UTM
    metrics = get_utm_metrics({"campaign": "spotify_launch_nov2025"})
    print("Métricas UTM:", metrics)
