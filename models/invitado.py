from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from utility.database import Base


class Invitado(Base):
    __tablename__ = "invitados"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String, nullable=False)

    confirmado = Column(Boolean, default=None)  # clave

    grupo_id = Column(Integer, ForeignKey("grupos.id"))

    grupo = relationship("Grupo", back_populates="invitados")