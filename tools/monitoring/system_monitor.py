"""
📊 SYSTEM MONITOR - Monitoreo de recursos
"""
import psutil
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemMonitor:
    def get_system_health(self):
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }
    
    def monitor_loop(self, interval=60):
        """Loop de monitoreo continuo"""
        logger.info("📊 System Monitor iniciado")
        
        while True:
            health = self.get_system_health()
            
            if health["cpu_percent"] > 90:
                logger.warning(f"⚠️ CPU HIGH: {health['cpu_percent']}%")
            
            if health["memory_percent"] > 85:
                logger.warning(f"⚠️ RAM HIGH: {health['memory_percent']}%")
            
            logger.info(f"📊 CPU: {health['cpu_percent']:.1f}% | RAM: {health['memory_percent']:.1f}%")
            
            time.sleep(interval)

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.monitor_loop(interval=30)
