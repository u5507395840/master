"""
YOLO v8 Analyzer - Análisis visual de contenido
"""
from typing import Dict, List
import os

class YOLOAnalyzer:
    def __init__(self):
        self.dummy_mode = os.getenv("DUMMY_MODE", "true").lower() == "true"
        self.model = None
        
        if not self.dummy_mode:
            try:
                from ultralytics import YOLO
                self.model = YOLO('yolov8n.pt')  # Nano model para velocidad
            except ImportError:
                print("⚠️ Ultralytics no instalado, usando dummy mode")
                self.dummy_mode = True
    
    def analyze_video(self, video_path: str) -> Dict:
        """Analizar video con YOLO v8"""
        
        if self.dummy_mode:
            return {
                "video_path": video_path,
                "detected_objects": ["person", "microphone", "studio", "lights"],
                "scene_type": "music_video",
                "visual_quality": 8.5,
                "viral_elements": ["neon_lights", "urban_setting", "artist_closeup"],
                "recommended_platforms": ["TikTok", "Instagram"],
                "timestamp_analysis": [
                    {"time": "0:05", "key_moment": "beat_drop", "engagement_potential": "high"},
                    {"time": "0:15", "key_moment": "hook", "engagement_potential": "very_high"},
                    {"time": "0:30", "key_moment": "transition", "engagement_potential": "medium"}
                ]
            }
        
        # Análisis real con YOLO
        results = self.model(video_path)
        
        detected_objects = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                detected_objects.append(self.model.names[cls])
        
        return {
            "video_path": video_path,
            "detected_objects": list(set(detected_objects)),
            "scene_type": self._classify_scene(detected_objects),
            "visual_quality": self._assess_quality(results)
        }
    
    def _classify_scene(self, objects: List[str]) -> str:
        """Clasificar tipo de escena"""
        if "person" in objects and "microphone" in objects:
            return "music_video"
        elif "person" in objects and "car" in objects:
            return "lifestyle"
        else:
            return "general"
    
    def _assess_quality(self, results) -> float:
        """Evaluar calidad visual"""
        # Implementación simplificada
        return 8.0
    
    def get_viral_clips(self, video_path: str, duration: int = 15) -> List[Dict]:
        """Identificar clips con mayor potencial viral"""
        
        return [
            {
                "start_time": 5,
                "end_time": 20,
                "viral_score": 9.2,
                "reason": "Beat drop + visual impact"
            },
            {
                "start_time": 30,
                "end_time": 45,
                "viral_score": 8.5,
                "reason": "Hook con letra pegajosa"
            }
        ]

# Instancia global
yolo_analyzer = YOLOAnalyzer()
