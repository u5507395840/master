"""
Metrics Viewer Component
Visualización de métricas en tiempo real
"""
import gradio as gr
from datetime import datetime, timedelta
from typing import Dict, List
import json

class MetricsViewer:
    """Componente para visualizar métricas de campañas"""
    
    def __init__(self, db_manager=None):
        self.db = db_manager
    
    def build(self) -> gr.Tab:
        """Construir el tab de métricas"""
        
        with gr.Tab("📊 Métricas") as tab:
            
            gr.Markdown("### Dashboard de Métricas en Tiempo Real")
            
            with gr.Row():
                # KPIs principales
                with gr.Column(scale=1):
                    gr.Markdown("#### 🎯 KPIs Principales")
                    
                    kpis_output = gr.Textbox(
                        label="Resumen General",
                        lines=15,
                        interactive=False
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("#### 📈 Performance")
                    
                    performance_output = gr.Textbox(
                        label="Métricas de Performance",
                        lines=15,
                        interactive=False
                    )
            
            gr.Markdown("---")
            
            # Campañas activas
            gr.Markdown("#### 🚀 Campañas Activas")
            
            campaigns_output = gr.Textbox(
                label="Listado de Campañas",
                lines=20,
                interactive=False
            )
            
            # Controles
            with gr.Row():
                refresh_btn = gr.Button("🔄 Actualizar Métricas", variant="primary")
                export_btn = gr.Button("📥 Exportar Datos", variant="secondary")
            
            # Auto-refresh cada 30 segundos
            auto_refresh = gr.Checkbox(
                label="♻️ Auto-actualizar (cada 30s)",
                value=False
            )
            
            # Conectar eventos
            refresh_btn.click(
                fn=self.get_all_metrics,
                outputs=[kpis_output, performance_output, campaigns_output]
            )
            
            export_btn.click(
                fn=self.export_metrics,
                outputs=gr.File(label="Descarga")
            )
            
            # Load inicial
            tab.load(
                fn=self.get_all_metrics,
                outputs=[kpis_output, performance_output, campaigns_output]
            )
        
        return tab
    
    def get_all_metrics(self) -> tuple:
        """Obtener todas las métricas"""
        
        # Obtener campañas de la DB (o mock)
        if self.db:
            try:
                campaigns = self.db.get_all_campaigns()
            except:
                campaigns = []
        else:
            campaigns = self._get_mock_campaigns()
        
        # Calcular KPIs
        kpis = self._calculate_kpis(campaigns)
        
        # Calcular performance
        performance = self._calculate_performance(campaigns)
        
        # Formatear campañas
        campaigns_text = self._format_campaigns_list(campaigns)
        
        return kpis, performance, campaigns_text
    
    def _calculate_kpis(self, campaigns: List[Dict]) -> str:
        """Calcular y formatear KPIs principales"""
        
        total_campaigns = len(campaigns)
        active_campaigns = sum(1 for c in campaigns if c.get('status') == 'active')
        
        total_reach = sum(
            c.get('metrics', {}).get('estimated_reach', 0) 
            for c in campaigns
        )
        
        total_views = sum(
            c.get('metrics', {}).get('current_views', 0)
            for c in campaigns
        )
        
        total_engagement = sum(
            c.get('metrics', {}).get('current_likes', 0) +
            c.get('metrics', {}).get('current_shares', 0)
            for c in campaigns
        )
        
        avg_viral_score = (
            sum(c.get('metrics', {}).get('viral_score', 0) for c in campaigns) / 
            max(total_campaigns, 1)
        )
        
        kpis_text = f"""
📊 RESUMEN GENERAL

🎯 Campañas Totales: {total_campaigns}
⚡ Campañas Activas: {active_campaigns}
💤 Pausadas/Finalizadas: {total_campaigns - active_campaigns}

════════════════════════════════════════

👥 ALCANCE

Reach Total: {total_reach:,} personas
Views Actuales: {total_views:,}
Promedio por Campaña: {int(total_views / max(total_campaigns, 1)):,}

════════════════════════════════════════

💬 ENGAGEMENT

Interacciones Totales: {total_engagement:,}
Engagement Rate: {(total_engagement / max(total_views, 1) * 100):.2f}%

════════════════════════════════════════

🔥 VIRAL SCORE

Promedio General: {avg_viral_score:.1f}/10
{self._get_score_emoji(avg_viral_score)}

════════════════════════════════════════

⏰ Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        """
        
        return kpis_text
    
    def _calculate_performance(self, campaigns: List[Dict]) -> str:
        """Calcular métricas de performance"""
        
        if not campaigns:
            return "📊 No hay datos de performance disponibles"
        
        # Performance por plataforma
        platform_stats = {}
        for campaign in campaigns:
            for platform in campaign.get('platforms', []):
                if platform not in platform_stats:
                    platform_stats[platform] = {
                        'campaigns': 0,
                        'reach': 0,
                        'engagement': 0
                    }
                platform_stats[platform]['campaigns'] += 1
                platform_stats[platform]['reach'] += campaign.get('metrics', {}).get('estimated_reach', 0)
        
        # Top performers
        sorted_campaigns = sorted(
            campaigns,
            key=lambda x: x.get('metrics', {}).get('viral_score', 0),
            reverse=True
        )[:5]
        
        performance_text = f"""
📈 PERFORMANCE POR PLATAFORMA

"""
        
        for platform, stats in sorted(platform_stats.items(), key=lambda x: x[1]['reach'], reverse=True):
            performance_text += f"""
📱 {platform}
   Campañas: {stats['campaigns']}
   Reach: {stats['reach']:,}
   Promedio: {int(stats['reach'] / max(stats['campaigns'], 1)):,}/campaña
"""
        
        performance_text += f"""

════════════════════════════════════════

🏆 TOP 5 CAMPAÑAS (por Viral Score)

"""
        
        for i, campaign in enumerate(sorted_campaigns, 1):
            performance_text += f"""
{i}. {campaign.get('artist')} - {campaign.get('track')}
   Score: {campaign.get('metrics', {}).get('viral_score', 0)}/10
   Reach: {campaign.get('metrics', {}).get('estimated_reach', 0):,}
   Estado: {campaign.get('status', 'unknown').upper()}
"""
        
        return performance_text
    
    def _format_campaigns_list(self, campaigns: List[Dict]) -> str:
        """Formatear lista de campañas"""
        
        if not campaigns:
            return """
📊 NO HAY CAMPAÑAS ACTIVAS

Lanza tu primera campaña en el tab "🚀 Lanzar Campaña"
            """
        
        # Ordenar por fecha (más recientes primero)
        sorted_campaigns = sorted(
            campaigns,
            key=lambda x: x.get('created_at', ''),
            reverse=True
        )
        
        campaigns_text = f"""
🚀 LISTADO DE CAMPAÑAS ({len(campaigns)} total)

════════════════════════════════════════════════════════════════

"""
        
        for campaign in sorted_campaigns:
            metrics = campaign.get('metrics', {})
            status_emoji = "✅" if campaign.get('status') == 'active' else "⏸️"
            
            campaigns_text += f"""
{status_emoji} {campaign.get('id')}

🎤 {campaign.get('artist')} - {campaign.get('track')}
🎸 Género: {campaign.get('genre')} | Mood: {campaign.get('mood')}
📱 Plataformas: {', '.join(campaign.get('platforms', []))}

📊 Métricas:
   👥 Reach: {metrics.get('estimated_reach', 0):,}
   👁️ Views: {metrics.get('current_views', 0):,}
   ❤️ Likes: {metrics.get('current_likes', 0):,}
   🔄 Shares: {metrics.get('current_shares', 0):,}
   🔥 Viral Score: {metrics.get('viral_score', 0)}/10

💰 Budget: ${campaign.get('budget', 0):,.2f}
📅 Duración: {campaign.get('duration', 0)} días
⏰ Creada: {self._format_date(campaign.get('created_at'))}

────────────────────────────────────────────────────────────────

"""
        
        return campaigns_text
    
    def export_metrics(self) -> str:
        """Exportar métricas a archivo JSON"""
        
        # Obtener todas las campañas
        if self.db:
            try:
                campaigns = self.db.get_all_campaigns()
            except:
                campaigns = []
        else:
            campaigns = self._get_mock_campaigns()
        
        # Crear archivo temporal
        filename = f"metrics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "total_campaigns": len(campaigns),
            "campaigns": campaigns
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def _get_mock_campaigns(self) -> List[Dict]:
        """Obtener campañas mock para testing"""
        return [
            {
                "id": "CAMP_20250109_001",
                "artist": "Bad Bunny",
                "track": "Tití Me Preguntó",
                "genre": "reggaeton",
                "mood": "fiestero",
                "platforms": ["TikTok", "Instagram Reels"],
                "budget": 1000,
                "duration": 7,
                "status": "active",
                "created_at": (datetime.now() - timedelta(days=2)).isoformat(),
                "metrics": {
                    "estimated_reach": 50000,
                    "current_views": 15234,
                    "current_likes": 1245,
                    "current_shares": 432,
                    "estimated_engagement": 8.5,
                    "viral_score": 8.7
                }
            },
            {
                "id": "CAMP_20250108_002",
                "artist": "Peso Pluma",
                "track": "Ella Baila Sola",
                "genre": "trap",
                "mood": "energético",
                "platforms": ["TikTok", "YouTube Shorts"],
                "budget": 500,
                "duration": 5,
                "status": "active",
                "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
                "metrics": {
                    "estimated_reach": 30000,
                    "current_views": 8450,
                    "current_likes": 892,
                    "current_shares": 234,
                    "estimated_engagement": 7.2,
                    "viral_score": 7.5
                }
            }
        ]
    
    def _get_score_emoji(self, score: float) -> str:
        """Obtener emoji según score"""
        if score >= 9:
            return "🔥🔥🔥 EXCELENTE"
        elif score >= 7:
            return "🔥🔥 MUY BUENO"
        elif score >= 5:
            return "🔥 BUENO"
        else:
            return "📊 REGULAR"
    
    def _format_date(self, date_str: str) -> str:
        """Formatear fecha ISO a legible"""
        try:
            dt = datetime.fromisoformat(date_str)
            return dt.strftime('%d/%m/%Y %H:%M')
        except:
            return "N/A"

