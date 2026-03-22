from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from utility.database import SessionLocal
from models.invitado import Invitado
from models.confirmacion import Confirmacion
from models.grupo import Grupo

router = APIRouter(
    prefix="/confirmacion",
    tags=["Confirmacion"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from utility.database import SessionLocal
from models.invitado import Invitado
from models.confirmacion import Confirmacion
from models.grupo import Grupo

@router.post("/{codigo}")
async def crear_confirmacion(codigo: int, request: Request, db: Session = Depends(get_db)):

    data = await request.json()

    grupo = db.query(Grupo).filter(Grupo.codigo == codigo).first()

    if not grupo:
        raise HTTPException(status_code=404, detail="Invitación inválida")

    confirmacion_existente = db.query(Confirmacion).filter(
        Confirmacion.grupo_id == grupo.id
    ).first()

    # =========================
    # 🟢 NUEVA CONFIRMACIÓN
    # =========================
    if not confirmacion_existente:

        confirmacion = Confirmacion(
            nombre_completo=data.get("nombre_completo"),
            correo=data.get("correo"),
            telefono=data.get("telefono"),
            asistira=True if data.get("asistira") else False,
            necesita_parqueadero=True if data.get("necesita_parqueadero") else False,
            cancion=data.get("cancion"),
            mensaje=data.get("mensaje"),
            grupo_id=grupo.id,
            reconfirmaciones=0
        )

        db.add(confirmacion)

    # =========================
    # 🟡 RECONFIRMAR
    # =========================
    else:

        confirmacion = confirmacion_existente

        if confirmacion.reconfirmaciones >= 1:
            raise HTTPException(
                status_code=400,
                detail="Ya realizaste una reconfirmación"
            )

        confirmacion.reconfirmaciones += 1

        confirmacion.nombre_completo = data.get("nombre_completo")
        confirmacion.correo = data.get("correo")
        confirmacion.telefono = data.get("telefono")
        confirmacion.asistira = True if data.get("asistira") else False
        confirmacion.necesita_parqueadero = True if data.get("necesita_parqueadero") else False
        confirmacion.cancion = data.get("cancion")
        confirmacion.mensaje = data.get("mensaje")

        # 🔥 FORZAR UPDATE TIMESTAMP
        confirmacion.updated_at = func.now()

    # =========================
    # 🔁 ACTUALIZAR INVITADOS
    # =========================
    for inv in data.get("invitados", []):
        invitado = db.query(Invitado).filter(
            Invitado.id == inv.get("id"),
            Invitado.grupo_id == grupo.id
        ).first()

        if invitado:
            invitado.confirmado = inv.get("confirmado", False)

    db.commit()

    return {"mensaje": "Confirmación registrada"}