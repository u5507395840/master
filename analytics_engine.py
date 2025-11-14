from fastapi import FastAPI

app = FastAPI(title="DOGMA ML Engine")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ml-engine"}

@app.get("/status")
async def status():
    return {"status": "running", "service": "dogma-ml", "version": "1.0.0"}

@app.post("/analyze/viral")
async def analyze_viral(video_url: str):
    # TODO: Integrar lógica YOLO aquí
    return {
        "viral_score": 0.0,
        "analysis": "pending",
        "message": "ML analysis not yet implemented"
    }

# Importar módulos ML si existen
try:
    from ml_engine.vision.yolo_analyzer import analyze_video
except ImportError:
    pass
