from pydantic import BaseModel, Field
from typing import Optional


class CoffinBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    material: str = Field(min_length=2, max_length=100)
    precio: float = Field(gt=0, description="Precio del ataúd (debe ser mayor a 0)")
    imagen_url: Optional[str] = None


class CoffinCreate(CoffinBase):
    pass


class CoffinUpdate(BaseModel):
    """Campos opcionales para actualización parcial."""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    material: Optional[str] = Field(None, min_length=2, max_length=100)
    precio: Optional[float] = Field(None, gt=0)
    imagen_url: Optional[str] = None


class CoffinResponse(CoffinBase):
    id: int
    model_config = {"from_attributes": True}


class PlanBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str = Field(min_length=2, max_length=500)
    precio_mensual: float = Field(gt=0, description="Precio mensual (debe ser mayor a 0)")


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    """Campos opcionales para actualización parcial."""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, min_length=2, max_length=500)
    precio_mensual: Optional[float] = Field(None, gt=0)


class PlanResponse(PlanBase):
    id: int
    model_config = {"from_attributes": True}