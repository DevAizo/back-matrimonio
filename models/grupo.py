from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from utility.database import Base


class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String, nullable=False)

    token = Column(String, unique=True, index=True)

    codigo = Column(Integer, unique=True)

    invitados = relationship("Invitado", back_populates="grupo")