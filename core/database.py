"""
Database Manager - SQLite para persistencia
Maneja campañas, métricas y logs
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class DatabaseManager:
    """Gestor de base de datos SQLite"""
    
    def __init__(self, db_path: str = "data/stakazo.db"):
        self.db_path = db_path
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Inicializar DB
        self._init_db()
    
    def _init_db(self):
        """Inicializar tablas de la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de campañas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                artist TEXT NOT NULL,
                track TEXT NOT NULL,
                genre TEXT,
                mood TEXT,
                platforms TEXT,
                budget REAL,
                duration INTEGER,
                video_url TEXT,
                video_prompt TEXT,
                target_age TEXT,
                target_gender TEXT,
                auto_optimize BOOLEAN,
                captions TEXT,
                hashtags TEXT,
                status TEXT,
                created_at TEXT,
                updated_at TEXT,
                metrics TEXT
            )
        """)
        
        # Tabla de métricas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id TEXT,
                timestamp TEXT,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                reach INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            )
        """)
        
        # Tabla de logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                level TEXT,
                module TEXT,
                message TEXT,
                data TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database initialized: {self.db_path}")
    
    def save_campaign(self, campaign: Dict) -> bool:
        """Guardar campaña en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO campaigns 
                (id, artist, track, genre, mood, platforms, budget, duration,
                 video_url, video_prompt, target_age, target_gender, auto_optimize,
                 captions, hashtags, status, created_at, updated_at, metrics)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                campaign['id'],
                campaign['artist'],
                campaign['track'],
                campaign.get('genre'),
                campaign.get('mood'),
                json.dumps(campaign.get('platforms', [])),
                campaign.get('budget', 0),
                campaign.get('duration', 0),
                campaign.get('video_url'),
                campaign.get('video_prompt'),
                json.dumps(campaign.get('target_age', [])),
                campaign.get('target_gender'),
                campaign.get('auto_optimize', False),
                json.dumps(campaign.get('captions', [])),
                json.dumps(campaign.get('hashtags', [])),
                campaign.get('status', 'active'),
                campaign.get('created_at', datetime.now().isoformat()),
                datetime.now().isoformat(),
                json.dumps(campaign.get('metrics', {}))
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error saving campaign: {e}")
            return False
    
    def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        """Obtener campaña por ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
            
        except Exception as e:
            print(f"❌ Error getting campaign: {e}")
            return None
    
    def get_all_campaigns(self, status: Optional[str] = None) -> List[Dict]:
        """Obtener todas las campañas"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if status:
                cursor.execute("SELECT * FROM campaigns WHERE status = ? ORDER BY created_at DESC", (status,))
            else:
                cursor.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
            
            rows = cursor.fetchall()
            conn.close()
            
            campaigns = []
            for row in rows:
                campaign = dict(row)
                # Deserializar JSON fields
                for field in ['platforms', 'target_age', 'captions', 'hashtags', 'metrics']:
                    if campaign.get(field):
                        try:
                            campaign[field] = json.loads(campaign[field])
                        except:
                            pass
                campaigns.append(campaign)
            
            return campaigns
            
        except Exception as e:
            print(f"❌ Error getting campaigns: {e}")
            return []
    
    def update_campaign_status(self, campaign_id: str, status: str) -> bool:
        """Actualizar estado de campaña"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE campaigns 
                SET status = ?, updated_at = ?
                WHERE id = ?
            """, (status, datetime.now().isoformat(), campaign_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error updating campaign: {e}")
            return False
    
    def save_metrics(self, campaign_id: str, metrics: Dict) -> bool:
        """Guardar métricas de campaña"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO metrics 
                (campaign_id, timestamp, views, likes, shares, comments, reach, engagement_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                campaign_id,
                datetime.now().isoformat(),
                metrics.get('views', 0),
                metrics.get('likes', 0),
                metrics.get('shares', 0),
                metrics.get('comments', 0),
                metrics.get('reach', 0),
                metrics.get('engagement_rate', 0)
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error saving metrics: {e}")
            return False
    
    def get_campaign_metrics(self, campaign_id: str) -> List[Dict]:
        """Obtener historial de métricas de campaña"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM metrics 
                WHERE campaign_id = ? 
                ORDER BY timestamp DESC
            """, (campaign_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"❌ Error getting metrics: {e}")
            return []
    
    def log(self, level: str, module: str, message: str, data: Optional[Dict] = None):
        """Guardar log en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO logs (timestamp, level, module, message, data)
                VALUES (?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                level,
                module,
                message,
                json.dumps(data) if data else None
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Error logging: {e}")
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas generales"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total de campañas
            cursor.execute("SELECT COUNT(*) FROM campaigns")
            total_campaigns = cursor.fetchone()[0]
            
            # Campañas activas
            cursor.execute("SELECT COUNT(*) FROM campaigns WHERE status = 'active'")
            active_campaigns = cursor.fetchone()[0]
            
            # Total de métricas registradas
            cursor.execute("SELECT COUNT(*) FROM metrics")
            total_metrics = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_campaigns": total_campaigns,
                "active_campaigns": active_campaigns,
                "paused_campaigns": total_campaigns - active_campaigns,
                "total_metrics_entries": total_metrics
            }
            
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return {}

# Instancia global
db = DatabaseManager()

