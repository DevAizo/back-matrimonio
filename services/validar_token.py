from sqlalchemy.orm import Session
from models.grupo import Grupo


def validar_token(db: Session, token: str):

    grupo = db.query(Grupo).filter(Grupo.token == token).first()

    if not grupo:
        return None

    return grupo