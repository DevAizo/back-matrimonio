import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔥 Tomar DATABASE_URL o fallback a MYSQL_URL
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL / MYSQL_URL no está configurada")

# 🔍 Mostrar URL sin password (debug seguro)
safe_url = DATABASE_URL.split("@")[-1]
print(f"🔥 Conectando a DB en: {safe_url}")

print("🔥 Iniciando conexión a DB...")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=3,
    max_overflow=5,
    pool_timeout=5,   # evita bloqueos largos
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