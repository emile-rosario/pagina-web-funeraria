"""
Router de carga de imágenes.
Permite subir imágenes y devuelve la URL pública.
"""
import logging
import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status

from app.security import get_current_admin

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Archivos"])

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    _admin=Depends(get_current_admin),
):
    """
    Subir una imagen (solo admin).
    Retorna la URL pública del archivo subido.
    """
    # Validar extensión
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensión no permitida. Usa: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Leer contenido y validar tamaño
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo excede el tamaño máximo de 5 MB.",
        )

    # Guardar con nombre único para evitar colisiones
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(content)

    logger.info("Imagen subida: %s (%d bytes)", unique_name, len(content))
    return {"filename": unique_name, "url": f"/uploads/{unique_name}"}
