from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# database
from utility.database import Base, engine

# modelos (IMPORTANTE para que SQLAlchemy los registre)
import models.grupo
import models.invitado
import models.confirmacion

# routers
from routers.invitacion import router as invitacion
from routers.confirmacion import router as confirmacion

app = FastAPI(
    title="API Matrimonio",
    description="Backend para confirmación de invitados",
    version="1.0"
)


# CORS para conectar con el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# registrar routers
app.include_router(invitacion)
app.include_router(confirmacion)


@app.get("/")
def root():
    return {"mensaje": "API de matrimonio funcionando"}