"""
Router de planes funerarios — CRUD completo.
GET es público; POST, PUT, DELETE requieren rol admin.
"""
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.funeral import Plan
from app.schemas.funeral import PlanCreate, PlanUpdate, PlanResponse
from app.security import get_current_admin, get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/planes", tags=["Planes Funerarios"])


@router.get("", response_model=list[PlanResponse])
def list_plans(db: Session = Depends(get_db)):
    """Listar todos los planes funerarios (público)."""
    return db.query(Plan).all()


@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    """Obtener un plan por ID (público)."""
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan no encontrado.",
        )
    return plan


@router.post("", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(
    data: PlanCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    """Crear un nuevo plan funerario (solo admin)."""
    plan = Plan(**data.model_dump())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    logger.info("Plan creado: %s (por admin)", plan.nombre)
    return plan


@router.put("/{plan_id}", response_model=PlanResponse)
def update_plan(
    plan_id: int,
    data: PlanUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    """Editar un plan existente (solo admin)."""
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan no encontrado.",
        )
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(plan, key, value)
    db.commit()
    db.refresh(plan)
    logger.info("Plan actualizado: ID %d", plan_id)
    return plan


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    """Eliminar un plan funerario (solo admin)."""
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan no encontrado.",
        )
    db.delete(plan)
    db.commit()
    logger.info("Plan eliminado: ID %d", plan_id)
