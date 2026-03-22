from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from utility.database import Base


class Confirmacion(Base):
    __tablename__ = "confirmaciones"

    id = Column(Integer, primary_key=True, index=True)

    nombre_completo = Column(String, nullable=False)

    correo = Column(String)
    telefono = Column(String)

    asistira = Column(Boolean, default=False)
    necesita_parqueadero = Column(Boolean, default=False)

    cancion = Column(String)
    mensaje = Column(String)

    grupo_id = Column(Integer, ForeignKey("grupos.id"), unique=True)

    reconfirmaciones = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())