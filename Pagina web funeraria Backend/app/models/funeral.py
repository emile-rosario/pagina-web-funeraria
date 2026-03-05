from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Plan(Base):
    __tablename__ = "planes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio_mensual = Column(Float)

class Coffin(Base):
    __tablename__ = "ataudes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    material = Column(String)
    precio = Column(Float)
    imagen_url = Column(String) # Aquí guardaremos la ruta de la foto que te dé el cliente