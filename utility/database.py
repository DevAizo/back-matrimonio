import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada")

print("🔥 Iniciando conexión a DB...")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=3,
    max_overflow=5,
    pool_timeout=5,  # 🔥 CLAVE: evita bloqueos esperando conexiones
    echo=True,       # 🔥 para ver qué pasa en logs
    connect_args={
        "connect_timeout": 5
    }
)

print("🔥 Engine creado correctamente")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()