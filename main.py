#!/usr/bin/env python3
"""
🎵 DISCOGRÁFICA ML PRO - MAIN INTERFACE
Sistema principal de lanzamiento y gestión de campañas virales
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para imports
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    """Interfaz principal del sistema"""
    print("🎵 DISCOGRÁFICA ML PRO - SISTEMA INICIALIZADO")
    print("="*60)
    
    try:
        # Importar y probar todos los módulos principales
        from core import start as core_start
        from ml_engine import load_model, evaluate_clip
        from campaign_manager import CampaignManager
        from uploaders import YouTubeUploader, MetaClient
        from security import get_env
        from analytics import start_dashboard
        from compliance import check_clip_duration
        
        print("✅ Todos los módulos cargados correctamente")
        
        # Ejecutar core
        print("\n🚀 Iniciando sistema core...")
        core_start()
        
        # Probar ML Engine
        print("\n🧠 Probando ML Engine...")
        load_model("test_model")
        evaluate_clip("test_clip.mp4")
        
        # Probar Campaign Manager
        print("\n📈 Probando Campaign Manager...")
        campaign_mgr = CampaignManager()
        campaign_mgr.create_campaign({"test": "campaign"})
        
        # Probar Uploaders
        print("\n📤 Probando Uploaders...")
        youtube = YouTubeUploader()
        meta = MetaClient()
        youtube.upload("test.mp4", "Test Video")
        meta.create_ad({"test": "ad"})
        
        # Probar Security
        print("\n🔒 Probando Security...")
        test_env = get_env("TEST_VAR", "default_value")
        print(f"Environment test: {test_env}")
        
        # Probar Analytics
        print("\n📊 Probando Analytics...")
        start_dashboard()
        
        # Probar Compliance
        print("\n⚖️ Probando Compliance...")
        compliance_result = check_clip_duration("test_clip.mp4")
        print(f"Compliance check: {compliance_result}")
        
        print("\n🎉 SISTEMA COMPLETAMENTE OPERATIVO")
        print("📋 Próximos pasos:")
        print("  1. Configurar tokens en .env")
        print("  2. Ejecutar auditoría: python scripts/audit_viral_marketing_ai.py")
        print("  3. Lanzar dashboards específicos")
        
        return 0
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Verifica que todos los módulos estén correctamente instalados")
        return 1
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        return 1

def show_help():
    """Muestra ayuda del sistema"""
    help_text = """
🎵 DISCOGRÁFICA ML PRO - AYUDA

USO:
    python main.py                    # Ejecutar sistema completo
    python main.py --help            # Mostrar esta ayuda
    python main.py --audit           # Ejecutar auditoría
    python main.py --test            # Ejecutar tests

MÓDULOS DISPONIBLES:
    core/                # Sistema principal
    ml_engine/           # Machine Learning y modelos
    campaign_manager/    # Gestión de campañas
    uploaders/           # APIs de YouTube, Meta, etc.
    security/            # Gestión de secretos
    analytics/           # Dashboards y métricas
    compliance/          # Verificaciones legales
    
SCRIPTS:
    scripts/audit_viral_marketing_ai.py    # Auditoría completa
    
CONFIGURACIÓN:
    .env                 # Variables de entorno
    requirements.txt     # Dependencias Python
    """
    print(help_text)

def run_audit():
    """Ejecuta la auditoría del sistema"""
    print("🔍 Ejecutando auditoría del sistema...")
    import subprocess
    result = subprocess.run([
        sys.executable, 
        "scripts/audit_viral_marketing_ai.py"
    ], cwd=PROJECT_ROOT)
    return result.returncode

def run_tests():
    """Ejecuta los tests del sistema"""
    print("🧪 Ejecutando tests...")
    import subprocess
    result = subprocess.run([
        sys.executable, 
        "-m", 
        "pytest", 
        "tests/"
    ], cwd=PROJECT_ROOT)
    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command in ["--help", "-h"]:
            show_help()
            sys.exit(0)
        elif command == "--audit":
            sys.exit(run_audit())
        elif command == "--test":
            sys.exit(run_tests())
        else:
            print(f"❌ Comando desconocido: {command}")
            print("💡 Usa --help para ver comandos disponibles")
            sys.exit(1)
    else:
        sys.exit(main())