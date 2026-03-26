from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload

from utility.database import SessionLocal
from models.grupo import Grupo
from models.confirmacion import Confirmacion


router = APIRouter(
    prefix="/invitacion",
    tags=["Invitacion"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{codigo}")
def obtener_invitacion(codigo: int, db: Session = Depends(get_db)):
    try:
        # 🔥 Trae grupo + invitados en una sola consulta
        grupo = (
            db.query(Grupo)
            .options(joinedload(Grupo.invitados))
            .filter(Grupo.codigo == codigo)
            .first()
        )

        if not grupo:
            raise HTTPException(status_code=404, detail="Invitación no válida")

        # 🔥 Buscar confirmación (protegido)
        confirmacion = (
            db.query(Confirmacion)
            .filter(Confirmacion.grupo_id == grupo.id)
            .first()
        )

        return {
            "grupo": grupo.nombre,

            "invitados": [
                {
                    "id": i.id,
                    "nombre": i.nombre,
                    "confirmado": i.confirmado
                }
                for i in grupo.invitados
            ],

            "confirmacion": {
                "nombre_completo": confirmacion.nombre_completo,
                "correo": confirmacion.correo,
                "telefono": confirmacion.telefono,
                "asistira": confirmacion.asistira,
                "necesita_parqueadero": confirmacion.necesita_parqueadero,
                "cancion": confirmacion.cancion,
                "mensaje": confirmacion.mensaje,
                "reconfirmaciones": confirmacion.reconfirmaciones
            } if confirmacion else None,

            "reconfirmaciones": confirmacion.reconfirmaciones if confirmacion else 0
        }

    except Exception as e:
        # 🔥 Esto evita que Railway te devuelva 503 sin explicación
        print("ERROR EN /invitacion:", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")