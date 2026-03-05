"""
Router de ataúdes — CRUD completo.
GET es público; POST, PUT, DELETE requieren rol admin.
"""
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.funeral import Coffin
from app.schemas.funeral import CoffinCreate, CoffinUpdate, CoffinResponse
from app.security import get_current_admin, get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ataudes", tags=["Ataúdes"])


@router.get("", response_model=list[CoffinResponse])
def list_coffins(db: Session = Depends(get_db)):
    """Listar todos los ataúdes (público)."""
    return db.query(Coffin).all()


@router.get("/{coffin_id}", response_model=CoffinResponse)
def get_coffin(coffin_id: int, db: Session = Depends(get_db)):
    """Obtener un ataúd por ID (público)."""
    coffin = db.query(Coffin).filter(Coffin.id == coffin_id).first()
    if not coffin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ataúd no encontrado.",
        )
    return coffin


@router.post("", response_model=CoffinResponse, status_code=status.HTTP_201_CREATED)
def create_coffin(
    data: CoffinCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    """Crear un nuevo ataúd (solo admin)."""
    coffin = Coffin(**data.model_dump())
    db.add(coffin)
    db.commit()
    db.refresh(coffin)
    logger.info("Ataúd creado: %s (por admin)", coffin.nombre)
    return coffin


@router.put("/{coffin_id}", response_model=CoffinResponse)
def update_coffin(
    coffin_id: int,
    data: CoffinUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    """Editar un ataúd existente (solo admin)."""
    coffin = db.query(Coffin).filter(Coffin.id == coffin_id).first()
    if not coffin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ataúd no encontrado.",
        )
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(coffin, key, value)
    db.commit()
    db.refresh(coffin)
    logger.info("Ataúd actualizado: ID %d", coffin_id)
    return coffin


@router.delete("/{coffin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coffin(
    coffin_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    """Eliminar un ataúd (solo admin)."""
    coffin = db.query(Coffin).filter(Coffin.id == coffin_id).first()
    if not coffin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ataúd no encontrado.",
        )
    db.delete(coffin)
    db.commit()
    logger.info("Ataúd eliminado: ID %d", coffin_id)
