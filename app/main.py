from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.routers import readings, dashboard
from app.config import settings

app = FastAPI(
    title="Weather Station API",
    description="Backend untuk 5 sensor cuaca (Neon + FastAPI)",
    version="1.0.0",
    debug=settings.APP_DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (untuk CSS/JS lokal nanti)
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include routers
app.include_router(readings.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"status": "healthy"}