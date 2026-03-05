"""
Backend Funeraria Rancier — Punto de entrada principal.
Configura la aplicación FastAPI, CORS, y registra los routers.
"""
import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base
from app.routers import auth, coffins, plans, uploads

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# --- App ---
app = FastAPI(
    title="Backend Funeraria Rancier",
    description="API para gestión de servicios funerarios, ataúdes y planes.",
    version="2.0.0",
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Archivos estáticos (imágenes subidas) ---
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# --- Crear tablas ---
Base.metadata.create_all(bind=engine)

# --- Registrar Routers ---
app.include_router(auth.router)
app.include_router(coffins.router)
app.include_router(plans.router)
app.include_router(uploads.router)


@app.get("/")
def root():
    """Health check — verifica que el backend está activo."""
    return {"message": "Backend de Funeraria Rancier Activo", "version": "2.0.0"}


logger.info("Backend Funeraria Rancier iniciado correctamente")