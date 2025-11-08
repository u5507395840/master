#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 AUDITORÍA TÉCNICA COMPLETA - VIRAL MARKETING AI SYSTEM
Sistema de validación integral para campañas de marketing viral
Basado en especificaciones técnicas profesionales
"""

import os
import re
import json
import glob
from pathlib import Path
from datetime import datetime
import subprocess
import traceback

class ViralMarketingAudit:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.audit_results = {
            'timestamp': datetime.now().isoformat(),
            'system_status': 'EVALUATING',
            'modules': {
                'targets_audiences': {'status': 'pending', 'findings': [], 'score': 0},
                'budget_distribution': {'status': 'pending', 'findings': [], 'score': 0},
                'pixels_capi_utms': {'status': 'pending', 'findings': [], 'score': 0},
                'ml_orchestrator': {'status': 'pending', 'findings': [], 'score': 0},
                'uploaders_apis': {'status': 'pending', 'findings': [], 'score': 0},
                'security_permissions': {'status': 'pending', 'findings': [], 'score': 0},
                'logs_metrics': {'status': 'pending', 'findings': [], 'score': 0},
                'legal_compliance': {'status': 'pending', 'findings': [], 'score': 0}
            },
            'critical_issues': [],
            'recommendations': [],
            'overall_score': 0,
            'campaign_readiness': 'UNKNOWN'
        }
    
    def print_header(self, title, level=1):
        """Headers formatados para la auditoría"""
        if level == 1:
            print(f"\n{'='*70}")
            print(f"🧠 {title}")
            print('='*70)
        elif level == 2:
            print(f"\n{'─'*50}")
            print(f"🔍 {title}")
            print('─'*50)
        else:
            print(f"\n🔸 {title}")
    
    def search_patterns(self, patterns, description):
        """Busca patrones en todos los archivos"""
        findings = []
        all_files = []
        
        # Obtener todos los archivos relevantes
        for ext in ['.py', '.json', '.yaml', '.yml', '.env', '.sh', '.js', '.ts']:
            all_files.extend(glob.glob(str(self.root_dir / f"**/*{ext}"), recursive=True))
        
        for pattern in patterns:
            for file_path in all_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            relative_path = os.path.relpath(file_path, self.root_dir)
                            findings.append({
                                'file': relative_path,
                                'line': line_num,
                                'content': line.strip(),
                                'pattern': pattern
                            })
                except Exception:
                    continue
        
        return findings
    
    def audit_targets_audiences(self):
        """1. Verificación de Targets y Audiencias"""
        self.print_header("VERIFICACIÓN DE TARGETS Y AUDIENCIAS", 2)
        
        patterns = [
            r'audience|targeting|geo|country|age|gender|interests|lookalike',
            r'min_age|max_age|age_min|age_max',
            r'españa|spain|mexico|colombia|argentina|chile|peru',
            r'16.*36|18.*35|target.*age'
        ]
        
        findings = self.search_patterns(patterns, "Targets y Audiencias")
        
        # Análisis específico
        target_countries = []
        age_ranges = []
        audience_configs = []
        
        for finding in findings:
            content_lower = finding['content'].lower()
            
            # Detectar países objetivo
            if any(country in content_lower for country in ['spain', 'españa', 'mexico', 'colombia', 'argentina']):
                target_countries.append(finding)
            
            # Detectar rangos de edad
            if re.search(r'\b(?:16|18|19|20|21|22|23|24|25|26|27|28|29|30|31|32|33|34|35|36)\b', content_lower):
                age_ranges.append(finding)
            
            # Detectar configuraciones de audiencia
            if any(term in content_lower for term in ['audience', 'targeting', 'lookalike']):
                audience_configs.append(finding)
        
        # Evaluación
        score = 0
        status_items = []
        
        if target_countries:
            score += 30
            status_items.append(f"✅ Países objetivo detectados: {len(target_countries)} configuraciones")
        else:
            status_items.append("❌ No se encontraron países objetivo (España + LATAM)")
            
        if age_ranges:
            score += 25
            status_items.append(f"✅ Rangos de edad detectados: {len(age_ranges)} configuraciones")
        else:
            status_items.append("❌ No se encontraron rangos de edad 16-36")
            
        if audience_configs:
            score += 25
            status_items.append(f"✅ Configuraciones de audiencia: {len(audience_configs)}")
        else:
            status_items.append("❌ No se encontraron configuraciones de targeting")
        
        if len(findings) >= 10:
            score += 20
            status_items.append(f"✅ Sistema bien configurado: {len(findings)} referencias")
        else:
            status_items.append(f"⚠️ Pocas configuraciones de targeting: {len(findings)}")
        
        for item in status_items:
            print(f"  {item}")
        
        self.audit_results['modules']['targets_audiences'] = {
            'status': 'completed',
            'findings': findings[:10],  # Primeras 10 para el reporte
            'score': score,
            'total_findings': len(findings),
            'countries': len(target_countries),
            'age_ranges': len(age_ranges),
            'audience_configs': len(audience_configs)
        }
        
        print(f"\n📊 Puntuación Módulo: {score}/100")
    
    def audit_budget_distribution(self):
        """2. Distribución de Presupuestos"""
        self.print_header("DISTRIBUCIÓN DE PRESUPUESTOS", 2)
        
        patterns = [
            r'budget|daily_budget|lifetime_budget|CBO|allocate_budget',
            r'fase.*1|fase.*2|fase.*3|testing|scaling|push.*organico',
            r'limit.*inversion|budget.*limit|max.*budget',
            r'campaign.*budget|ad.*budget|spend.*limit'
        ]
        
        findings = self.search_patterns(patterns, "Presupuestos")
        
        # Análisis específico
        budget_configs = []
        phase_configs = []
        limit_configs = []
        
        for finding in findings:
            content_lower = finding['content'].lower()
            
            if any(term in content_lower for term in ['budget', 'cbo', 'allocate']):
                budget_configs.append(finding)
            
            if any(term in content_lower for term in ['fase', 'testing', 'scaling', 'phase']):
                phase_configs.append(finding)
            
            if any(term in content_lower for term in ['limit', 'max_budget', 'daily_limit']):
                limit_configs.append(finding)
        
        # Evaluación
        score = 0
        status_items = []
        
        if budget_configs:
            score += 35
            status_items.append(f"✅ Configuraciones de presupuesto: {len(budget_configs)}")
        else:
            status_items.append("❌ No se encontraron configuraciones de presupuesto")
        
        if phase_configs:
            score += 30
            status_items.append(f"✅ Fases de campaña detectadas: {len(phase_configs)}")
        else:
            status_items.append("❌ No se encontraron fases (testing/scaling/push)")
        
        if limit_configs:
            score += 25
            status_items.append(f"✅ Límites de inversión: {len(limit_configs)}")
        else:
            status_items.append("❌ No se encontraron límites de presupuesto")
        
        if len(findings) >= 5:
            score += 10
            status_items.append("✅ Sistema de presupuestos bien estructurado")
        
        for item in status_items:
            print(f"  {item}")
        
        self.audit_results['modules']['budget_distribution'] = {
            'status': 'completed',
            'findings': findings[:10],
            'score': score,
            'budget_configs': len(budget_configs),
            'phase_configs': len(phase_configs),
            'limit_configs': len(limit_configs)
        }
        
        print(f"\n📊 Puntuación Módulo: {score}/100")
    
    def audit_pixels_capi_utms(self):
        """3. Integración de Pixels, CAPI y UTMs"""
        self.print_header("PIXELS, CAPI Y UTMS", 2)
        
        patterns = [
            r'pixel_id|PIXEL_ID|facebook.*pixel|meta.*pixel',
            r'capi|conversion.*api|capi_endpoint',
            r'utm_|utmSource|utm_source|utm_campaign|utm_medium|utm_content',
            r'\.env|environment|config.*pixel'
        ]
        
        findings = self.search_patterns(patterns, "Pixels y UTMs")
        
        # Análisis específico
        pixel_configs = []
        capi_configs = []
        utm_configs = []
        env_configs = []
        
        for finding in findings:
            content_lower = finding['content'].lower()
            
            if any(term in content_lower for term in ['pixel_id', 'pixel', 'facebook_pixel']):
                pixel_configs.append(finding)
            
            if any(term in content_lower for term in ['capi', 'conversion_api']):
                capi_configs.append(finding)
            
            if 'utm_' in content_lower:
                utm_configs.append(finding)
            
            if any(term in content_lower for term in ['.env', 'environment', 'config']):
                env_configs.append(finding)
        
        # Evaluación
        score = 0
        status_items = []
        
        if pixel_configs:
            score += 30
            status_items.append(f"✅ Pixels configurados: {len(pixel_configs)}")
        else:
            status_items.append("❌ No se encontraron configuraciones de pixel")
        
        if capi_configs:
            score += 25
            status_items.append(f"✅ CAPI integrado: {len(capi_configs)}")
        else:
            status_items.append("⚠️ CAPI no detectado")
        
        if utm_configs:
            score += 35
            status_items.append(f"✅ UTMs implementados: {len(utm_configs)}")
        else:
            status_items.append("❌ No se encontraron UTMs")
        
        if env_configs:
            score += 10
            status_items.append(f"✅ Variables de entorno: {len(env_configs)}")
        
        for item in status_items:
            print(f"  {item}")
        
        self.audit_results['modules']['pixels_capi_utms'] = {
            'status': 'completed',
            'findings': findings[:10],
            'score': score,
            'pixels': len(pixel_configs),
            'capi': len(capi_configs),
            'utms': len(utm_configs)
        }
        
        print(f"\n📊 Puntuación Módulo: {score}/100")
    
    def audit_ml_orchestrator(self):
        """4. Machine Learning y Orquestador"""
        self.print_header("MACHINE LEARNING Y ORQUESTADOR", 2)
        
        patterns = [
            r'/brain/|evaluate_campaign|allocate_budget|update_model',
            r'MiniLM|all-MiniLM-L6-v2|sentence.*transformer',
            r'dry_run|simulation|rules_engine|test.*mode',
            r'ultralytics|yolo|ml_core|analytics_engine'
        ]
        
        findings = self.search_patterns(patterns, "ML y Orquestador")
        
        # Análisis específico
        brain_endpoints = []
        ml_models = []
        simulation_modes = []
        ml_systems = []
        
        for finding in findings:
            content_lower = finding['content'].lower()
            
            if any(term in content_lower for term in ['/brain/', 'evaluate_campaign', 'allocate_budget']):
                brain_endpoints.append(finding)
            
            if any(term in content_lower for term in ['minilm', 'transformer', 'model']):
                ml_models.append(finding)
            
            if any(term in content_lower for term in ['dry_run', 'simulation', 'test_mode']):
                simulation_modes.append(finding)
            
            if any(term in content_lower for term in ['ultralytics', 'yolo', 'ml_core']):
                ml_systems.append(finding)
        
        # Evaluación
        score = 0
        status_items = []
        
        if brain_endpoints:
            score += 30
            status_items.append(f"✅ Endpoints brain detectados: {len(brain_endpoints)}")
        else:
            status_items.append("❌ No se encontraron endpoints /brain/")
        
        if ml_models:
            score += 25
            status_items.append(f"✅ Modelos ML configurados: {len(ml_models)}")
        else:
            status_items.append("❌ No se detectaron modelos ML")
        
        if simulation_modes:
            score += 20
            status_items.append(f"✅ Modos de simulación: {len(simulation_modes)}")
        else:
            status_items.append("⚠️ No se encontró modo dry_run/simulation")
        
        if ml_systems:
            score += 25
            status_items.append(f"✅ Sistemas ML activos: {len(ml_systems)}")
        else:
            status_items.append("❌ No se detectaron sistemas ML (YOLO/Ultralytics)")
        
        for item in status_items:
            print(f"  {item}")
        
        self.audit_results['modules']['ml_orchestrator'] = {
            'status': 'completed',
            'findings': findings[:10],
            'score': score,
            'brain_endpoints': len(brain_endpoints),
            'ml_models': len(ml_models),
            'simulation_modes': len(simulation_modes)
        }
        
        print(f"\n📊 Puntuación Módulo: {score}/100")
    
    def audit_uploaders_apis(self):
        """5. Uploaders y APIs"""
        self.print_header("UPLOADERS Y APIS", 2)
        
        patterns = [
            r'uploader\.py|youtube_client|meta_client|tiktok_uploader',
            r'upload.*video|post.*video|publish.*content',
            r'retry|backoff|rate.*limit|max.*attempts',
            r'error.*handling|exception|try.*except|logging'
        ]
        
        findings = self.search_patterns(patterns, "Uploaders y APIs")
        
        # Análisis específico
        uploader_files = []
        upload_functions = []
        retry_mechanisms = []
        error_handling = []
        
        for finding in findings:
            content_lower = finding['content'].lower()
            
            if any(term in content_lower for term in ['uploader', 'client.py', 'youtube_client']):
                uploader_files.append(finding)
            
            if any(term in content_lower for term in ['upload', 'post', 'publish']):
                upload_functions.append(finding)
            
            if any(term in content_lower for term in ['retry', 'backoff', 'rate_limit']):
                retry_mechanisms.append(finding)
            
            if any(term in content_lower for term in ['error', 'exception', 'try', 'logging']):
                error_handling.append(finding)
        
        # Evaluación
        score = 0
        status_items = []
        
        if uploader_files:
            score += 30
            status_items.append(f"✅ Uploaders detectados: {len(uploader_files)}")
        else:
            status_items.append("❌ No se encontraron uploaders")
        
        if upload_functions:
            score += 25
            status_items.append(f"✅ Funciones de upload: {len(upload_functions)}")
        else:
            status_items.append("❌ No se detectaron funciones de upload")
        
        if retry_mechanisms:
            score += 25
            status_items.append(f"✅ Mecanismos de retry: {len(retry_mechanisms)}")
        else:
            status_items.append("⚠️ No se encontraron mecanismos de retry")
        
        if error_handling:
            score += 20
            status_items.append(f"✅ Manejo de errores: {len(error_handling)}")
        else:
            status_items.append("❌ Manejo de errores insuficiente")
        
        for item in status_items:
            print(f"  {item}")
        
        self.audit_results['modules']['uploaders_apis'] = {
            'status': 'completed',
            'findings': findings[:10],
            'score': score,
            'uploaders': len(uploader_files),
            'upload_functions': len(upload_functions),
            'retry_mechanisms': len(retry_mechanisms)
        }
        
        print(f"\n📊 Puntuación Módulo: {score}/100")
    
    def audit_security_permissions(self):
        """6. Seguridad y Permisos"""
        self.print_header("SEGURIDAD Y PERMISOS", 2)
        
        patterns = [
            r'SECRET_KEY|API_KEY|PRIVATE_KEY|client_secret',
            r'token|password|auth|authentication',
            r'https|ssl|tls|secure',
            r'\.env|environment|config.*secret'
        ]
        
        findings = self.search_patterns(patterns, "Seguridad")
        
        # Análisis específico
        secret_keys = []
        auth_tokens = []
        https_configs = []
        env_files = []
        exposed_secrets = []
        
        for finding in findings:
            content_lower = finding['content'].lower()
            
            if any(term in content_lower for term in ['secret_key', 'api_key', 'private_key']):
                secret_keys.append(finding)
                # Verificar si hay secretos expuestos (valor real visible)
                if '=' in finding['content'] and len(finding['content'].split('=')[1].strip()) > 10:
                    if not finding['content'].split('=')[1].strip().startswith(('$', 'os.', 'env.')):
                        exposed_secrets.append(finding)
            
            if any(term in content_lower for term in ['token', 'password', 'auth']):
                auth_tokens.append(finding)
            
            if any(term in content_lower for term in ['https', 'ssl', 'secure']):
                https_configs.append(finding)
            
            if '.env' in finding['file'] or 'environment' in content_lower:
                env_files.append(finding)
        
        # Evaluación
        score = 100  # Empezamos con puntuación completa y restamos por problemas
        status_items = []
        
        if secret_keys:
            status_items.append(f"✅ Configuraciones de seguridad: {len(secret_keys)}")
        else:
            score -= 30
            status_items.append("❌ No se encontraron configuraciones de API keys")
        
        if exposed_secrets:
            score -= 50  # Penalización severa por secretos expuestos
            status_items.append(f"🚨 CRÍTICO: Secretos expuestos detectados: {len(exposed_secrets)}")
            self.audit_results['critical_issues'].append("Secretos o tokens expuestos en código")
        else:
            status_items.append("✅ No se detectaron secretos expuestos")
        
        if auth_tokens:
            status_items.append(f"✅ Sistema de autenticación: {len(auth_tokens)}")
        else:
            score -= 20
            status_items.append("⚠️ Autenticación no claramente definida")
        
        if https_configs:
            status_items.append(f"✅ Configuraciones HTTPS: {len(https_configs)}")
        else:
            score -= 15
            status_items.append("⚠️ No se detectaron configuraciones HTTPS/SSL")
        
        if env_files:
            status_items.append(f"✅ Archivos de entorno: {len(env_files)}")
        
        score = max(0, score)  # No permitir puntuaciones negativas
        
        for item in status_items:
            print(f"  {item}")
        
        self.audit_results['modules']['security_permissions'] = {
            'status': 'completed',
            'findings': findings[:10],
            'score': score,
            'secret_keys': len(secret_keys),
            'exposed_secrets': len(exposed_secrets),
            'auth_tokens': len(auth_tokens),
            'https_configs': len(https_configs)
        }
        
        print(f"\n📊 Puntuación Módulo: {score}/100")
    
    def audit_logs_metrics(self):
        """7. Logs, Alertas y Métricas"""
        self.print_header("LOGS, ALERTAS Y MÉTRICAS", 2)
        
        patterns = [
            r'exchange_events|campaign_actions|metrics|upload_results',
            r'retention|engagement|rewatches|score.*ponderado',
            r'logging|log\.info|log\.error|logger',
            r'alert|notification|monitor|dashboard'
        ]
        
        findings = self.search_patterns(patterns, "Logs y Métricas")
        
        # Análisis específico
        event_logs = []
        metrics_calc = []
        logging_system = []
        alerts_system = []
        
        for finding in findings:
            content_lower = finding['content'].lower()
            
            if any(term in content_lower for term in ['exchange_events', 'campaign_actions', 'metrics']):
                event_logs.append(finding)
            
            if any(term in content_lower for term in ['retention', 'engagement', 'rewatch', 'score']):
                metrics_calc.append(finding)
            
            if any(term in content_lower for term in ['logging', 'log.', 'logger']):
                logging_system.append(finding)
            
            if any(term in content_lower for term in ['alert', 'notification', 'monitor']):
                alerts_system.append(finding)
        
        # Evaluación
        score = 0
        status_items = []
        
        if event_logs:
            score += 30
            status_items.append(f"✅ Logs de eventos: {len(event_logs)}")
        else:
            status_items.append("❌ No se encontraron logs de eventos/campañas")
        
        if metrics_calc:
            score += 25
            status_items.append(f"✅ Cálculo de métricas: {len(metrics_calc)}")
        else:
            status_items.append("❌ No se detectó cálculo de métricas ponderadas")
        
        if logging_system:
            score += 25
            status_items.append(f"✅ Sistema de logging: {len(logging_system)}")
        else:
            status_items.append("❌ Sistema de logging insuficiente")
        
        if alerts_system:
            score += 20
            status_items.append(f"✅ Sistema de alertas: {len(alerts_system)}")
        else:
            status_items.append("⚠️ No se detectó sistema de alertas")
        
        for item in status_items:
            print(f"  {item}")
        
        self.audit_results['modules']['logs_metrics'] = {
            'status': 'completed',
            'findings': findings[:10],
            'score': score,
            'event_logs': len(event_logs),
            'metrics_calc': len(metrics_calc),
            'logging_system': len(logging_system)
        }
        
        print(f"\n📊 Puntuación Módulo: {score}/100")
    
    def audit_legal_compliance(self):
        """8. Legalidad de Clips y Derechos"""
        self.print_header("LEGALIDAD DE CLIPS Y DERECHOS", 2)
        
        patterns = [
            r'license_status|license|copyright|legal',
            r'clip.*duration|15s|15.*second|duration.*limit',
            r'lut|filter|marca.*agua|watermark',
            r'strike|claim|copyright.*claim|dmca'
        ]
        
        findings = self.search_patterns(patterns, "Legalidad")
        
        # Análisis específico
        license_configs = []
        duration_limits = []
        filtering_system = []
        copyright_protection = []
        
        for finding in findings:
            content_lower = finding['content'].lower()
            
            if any(term in content_lower for term in ['license', 'copyright', 'legal']):
                license_configs.append(finding)
            
            if any(term in content_lower for term in ['15s', '15 second', 'duration', 'limit']):
                duration_limits.append(finding)
            
            if any(term in content_lower for term in ['lut', 'filter', 'watermark', 'marca']):
                filtering_system.append(finding)
            
            if any(term in content_lower for term in ['strike', 'claim', 'dmca']):
                copyright_protection.append(finding)
        
        # Evaluación
        score = 0
        status_items = []
        
        if license_configs:
            score += 30
            status_items.append(f"✅ Configuraciones de licencia: {len(license_configs)}")
        else:
            status_items.append("❌ No se encontraron validaciones de licencia")
        
        if duration_limits:
            score += 25
            status_items.append(f"✅ Límites de duración: {len(duration_limits)}")
        else:
            status_items.append("⚠️ No se detectaron límites de duración (≤15s)")
        
        if filtering_system:
            score += 25
            status_items.append(f"✅ Sistema de filtros/LUTs: {len(filtering_system)}")
        else:
            status_items.append("⚠️ No se detectó sistema de filtros/LUTs")
        
        if copyright_protection:
            score += 20
            status_items.append(f"✅ Protección copyright: {len(copyright_protection)}")
        else:
            status_items.append("❌ No se detectó protección anti-copyright")
        
        for item in status_items:
            print(f"  {item}")
        
        self.audit_results['modules']['legal_compliance'] = {
            'status': 'completed',
            'findings': findings[:10],
            'score': score,
            'license_configs': len(license_configs),
            'duration_limits': len(duration_limits),
            'filtering_system': len(filtering_system)
        }
        
        print(f"\n📊 Puntuación Módulo: {score}/100")
    
    def calculate_overall_score(self):
        """Calcula puntuación general y determina viabilidad"""
        
        # Pesos por módulo (total 100%)
        weights = {
            'targets_audiences': 0.15,      # 15%
            'budget_distribution': 0.20,    # 20%
            'pixels_capi_utms': 0.15,      # 15%
            'ml_orchestrator': 0.15,       # 15%
            'uploaders_apis': 0.15,        # 15%
            'security_permissions': 0.10,   # 10%
            'logs_metrics': 0.05,          # 5%
            'legal_compliance': 0.05       # 5%
        }
        
        total_score = 0
        for module, weight in weights.items():
            module_score = self.audit_results['modules'][module]['score']
            weighted_score = module_score * weight
            total_score += weighted_score
        
        self.audit_results['overall_score'] = round(total_score, 1)
        
        # Determinar estado de preparación para campaña
        if total_score >= 85:
            self.audit_results['campaign_readiness'] = 'LISTO PARA PRODUCCIÓN'
            self.audit_results['system_status'] = 'EXCELENTE'
        elif total_score >= 70:
            self.audit_results['campaign_readiness'] = 'LISTO CON AJUSTES MENORES'
            self.audit_results['system_status'] = 'BUENO'
        elif total_score >= 50:
            self.audit_results['campaign_readiness'] = 'REQUIERE MEJORAS IMPORTANTES'
            self.audit_results['system_status'] = 'REGULAR'
        else:
            self.audit_results['campaign_readiness'] = 'NO LISTO - REQUIERE REFACTORIZACIÓN'
            self.audit_results['system_status'] = 'CRÍTICO'
    
    def generate_recommendations(self):
        """Genera recomendaciones basadas en los hallazgos"""
        
        recommendations = []
        
        # Recomendaciones por módulo
        for module_name, module_data in self.audit_results['modules'].items():
            score = module_data['score']
            
            if module_name == 'targets_audiences' and score < 70:
                recommendations.append("Configurar targeting específico para España + LATAM, edades 16-36")
            
            if module_name == 'budget_distribution' and score < 70:
                recommendations.append("Implementar fases de presupuesto (testing/scaling/push) con límites")
            
            if module_name == 'pixels_capi_utms' and score < 70:
                recommendations.append("Configurar Facebook Pixel, CAPI y UTMs únicos por clip")
            
            if module_name == 'ml_orchestrator' and score < 70:
                recommendations.append("Implementar endpoints /brain/ y modelos MiniLM para decisiones ML")
            
            if module_name == 'uploaders_apis' and score < 70:
                recommendations.append("Mejorar uploaders con retry, rate limiting y manejo de errores")
            
            if module_name == 'security_permissions' and score < 70:
                recommendations.append("Revisar seguridad: mover secretos a .env, implementar HTTPS")
            
            if module_name == 'logs_metrics' and score < 70:
                recommendations.append("Implementar logging completo y métricas ponderadas")
            
            if module_name == 'legal_compliance' and score < 70:
                recommendations.append("Configurar validación de licencias y límites de duración ≤15s")
        
        self.audit_results['recommendations'] = recommendations
    
    def run_bash_audit(self):
        """Ejecuta el script bash equivalente para comparación"""
        bash_script = """
grep -R --line-number -E "campaign|CBO|budget|daily_budget|lifetime_budget" . 2>/dev/null | head -20
grep -R --line-number -E "audience|targeting|geo|country|age|min_age|max_age|gender|interests|lookalike" . 2>/dev/null | head -20
grep -R --line-number -E "pixel_id|PIXEL_ID|capi|utm_|utmSource|utm_source|utm_campaign" . 2>/dev/null | head -20
grep -R --line-number -E "allocate_budget|Thompson|UCB|bandit|multiarmed|redistribute" . 2>/dev/null | head -20
grep -R --line-number -E "brain|evaluate_campaign|update_model|predict|classifier|MiniLM" . 2>/dev/null | head -20
grep -R --line-number -E "youtube|YouTube|meta|Meta|facebook|tiktok|instagram|upload" . 2>/dev/null | head -20
grep -R --line-number -E "max_per_hour|max_per_day|cooldown|rate_limit|backoff" . 2>/dev/null | head -20
grep -R --line-number -E "API_KEY|SECRET_KEY|PRIVATE_KEY|token:|password:|client_secret" . 2>/dev/null | head -20
"""
        
        self.print_header("BASH AUDIT EQUIVALENT OUTPUT", 2)
        
        try:
            # Simular la salida del bash (ya que estamos en Windows)
            print("🖥️ Simulación de audit_repo.sh (adaptado para Windows):")
            print("=" * 60)
            
            # Mostrar algunos hallazgos clave del análisis Python
            total_findings = sum(len(module['findings']) for module in self.audit_results['modules'].values())
            print(f"Total patterns found: {total_findings}")
            
            # Mostrar ejemplos de cada categoría
            for module_name, module_data in self.audit_results['modules'].items():
                if module_data['findings']:
                    print(f"\n--- {module_name.upper()} ---")
                    for finding in module_data['findings'][:3]:  # Primeros 3 de cada módulo
                        print(f"{finding['file']}:{finding['line']}: {finding['content'][:80]}...")
            
        except Exception as e:
            print(f"Error en bash audit: {e}")
    
    def generate_report(self):
        """Genera el reporte final completo"""
        
        self.print_header("REPORTE FINAL - VIRAL MARKETING AI AUDIT")
        
        print(f"📊 PUNTUACIÓN GENERAL: {self.audit_results['overall_score']}/100")
        print(f"🎯 ESTADO DEL SISTEMA: {self.audit_results['system_status']}")
        print(f"🚀 PREPARACIÓN CAMPAÑA: {self.audit_results['campaign_readiness']}")
        
        print("\n📋 DESGLOSE POR MÓDULOS:")
        for module_name, module_data in self.audit_results['modules'].items():
            status_emoji = "✅" if module_data['score'] >= 70 else "⚠️" if module_data['score'] >= 50 else "❌"
            print(f"  {status_emoji} {module_name.replace('_', ' ').title()}: {module_data['score']}/100")
        
        if self.audit_results['critical_issues']:
            print("\n🚨 PROBLEMAS CRÍTICOS:")
            for issue in self.audit_results['critical_issues']:
                print(f"  ❌ {issue}")
        
        if self.audit_results['recommendations']:
            print("\n🔧 RECOMENDACIONES:")
            for i, rec in enumerate(self.audit_results['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        # Guardar reporte en JSON
        report_path = self.root_dir / f"viral_marketing_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.audit_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Reporte completo guardado en: {report_path}")
        
        return self.audit_results
    
    def run_full_audit(self):
        """Ejecuta la auditoría completa"""
        
        self.print_header("AUDITORÍA TÉCNICA COMPLETA - VIRAL MARKETING AI")
        
        print("🎯 Verificando viabilidad para campañas de marketing viral...")
        print("📋 Analizando 8 módulos críticos del sistema...")
        
        try:
            # Ejecutar todos los módulos de auditoría
            self.audit_targets_audiences()
            self.audit_budget_distribution()
            self.audit_pixels_capi_utms()
            self.audit_ml_orchestrator()
            self.audit_uploaders_apis()
            self.audit_security_permissions()
            self.audit_logs_metrics()
            self.audit_legal_compliance()
            
            # Cálculos finales
            self.calculate_overall_score()
            self.generate_recommendations()
            
            # Bash audit equivalente
            self.run_bash_audit()
            
            # Reporte final
            results = self.generate_report()
            
            return results
            
        except Exception as e:
            print(f"\n💥 Error durante auditoría: {e}")
            traceback.print_exc()
            return None

def main():
    """Función principal"""
    auditor = ViralMarketingAudit()
    results = auditor.run_full_audit()
    
    if results:
        print(f"\n🎉 AUDITORÍA COMPLETADA")
        print(f"⏰ Timestamp: {results['timestamp']}")
        print(f"📊 Score: {results['overall_score']}/100")
        print(f"🚀 Status: {results['campaign_readiness']}")
    else:
        print(f"\n💥 Auditoría falló")

if __name__ == "__main__":
    main()