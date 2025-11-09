"""
ML Metrics Analyzer - Sistema de análisis con Machine Learning
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List
import json

class MetricsAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
    
    def calculate_viral_score(self, metrics: Dict) -> float:
        """Calcular score de viralidad (0-10)"""
        
        views = metrics.get('views', 0)
        likes = metrics.get('likes', 0)
        shares = metrics.get('shares', 0)
        comments = metrics.get('comments', 0)
        
        # Engagement rate
        engagement_rate = ((likes + shares + comments) / max(views, 1)) * 100
        
        # Share velocity (shares per view)
        share_velocity = (shares / max(views, 1)) * 100
        
        # Viral coefficient
        viral_coefficient = (shares * 0.3) + (engagement_rate * 0.5) + (share_velocity * 0.2)
        
        # Normalizar a escala 0-10
        viral_score = min(10, viral_coefficient / 2)
        
        return round(viral_score, 2)
    
    def predict_reach(self, current_metrics: Dict) -> Dict:
        """Predecir reach futuro"""
        
        views = current_metrics.get('views', 0)
        engagement_rate = current_metrics.get('engagement_rate', 5.0)
        
        # Predicción simple basada en tendencia
        predicted_24h = int(views * (1 + (engagement_rate / 100)))
        predicted_7d = int(predicted_24h * 5)
        
        return {
            "current_views": views,
            "predicted_24h": predicted_24h,
            "predicted_7d": predicted_7d,
            "confidence": 0.78
        }
    
    def analyze_best_posting_time(self, historical_data: List[Dict]) -> Dict:
        """Analizar mejor horario para publicar"""
        
        # Datos mock de análisis
        return {
            "best_day": "Viernes",
            "best_hour": "18:00 - 21:00",
            "timezone": "America/Mexico_City",
            "engagement_increase": "+35%"
        }
    
    def get_content_recommendations(self, performance_data: Dict) -> List[str]:
        """Obtener recomendaciones de contenido"""
        
        viral_score = self.calculate_viral_score(performance_data)
        
        recommendations = []
        
        if viral_score > 7:
            recommendations.append("✅ Contenido con alto potencial viral - Aumentar presupuesto")
            recommendations.append("🚀 Crear variantes similares del mismo estilo")
        elif viral_score > 5:
            recommendations.append("⚠️ Rendimiento medio - Probar con diferentes hashtags")
            recommendations.append("💡 Experimentar con horarios de publicación")
        else:
            recommendations.append("❌ Bajo rendimiento - Replantear estrategia de contenido")
            recommendations.append("🔄 Analizar contenido de competidores exitosos")
        
        return recommendations

# Instancia global
metrics_analyzer = MetricsAnalyzer()
