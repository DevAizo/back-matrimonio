import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # evita conexiones muertas
    pool_recycle=300,        # reinicia conexiones cada 5 min
    pool_size=5,             # conexiones base
    max_overflow=10,         # conexiones extra
    connect_args={
        "connect_timeout": 10  # evita que se cuelgue 15s+
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()