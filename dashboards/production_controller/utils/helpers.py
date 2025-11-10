"""
Helper functions para el dashboard
"""
from datetime import datetime
from typing import Dict, Any

def format_number(num: int) -> str:
    """Formatear número con comas"""
    return f"{num:,}"

def format_currency(amount: float) -> str:
    """Formatear como moneda"""
    return f"${amount:,.2f}"

def format_percentage(value: float) -> str:
    """Formatear como porcentaje"""
    return f"{value:.2f}%"

def format_datetime(dt: datetime) -> str:
    """Formatear fecha/hora"""
    return dt.strftime('%d/%m/%Y %H:%M:%S')

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncar texto con ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def validate_campaign_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """Validar datos de campaña"""
    
    required_fields = ['artist', 'track', 'genre', 'platforms']
    
    for field in required_fields:
        if not data.get(field):
            return False, f"Campo requerido: {field}"
    
    if not data.get('platforms'):
        return False, "Selecciona al menos una plataforma"
    
    if data.get('budget', 0) < 0:
        return False, "El budget no puede ser negativo"
    
    if data.get('duration', 0) <= 0:
        return False, "La duración debe ser mayor a 0"
    
    return True, "OK"

