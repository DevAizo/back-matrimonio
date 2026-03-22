# scripts/cargar_invitados.py

import pandas as pd
import secrets
import string

from sqlalchemy.orm import Session

from utility.database import SessionLocal
from models.grupo import Grupo
from models.invitado import Invitado


EXCEL_PATH = "invitados.xlsx"  # <-- ajusta si tu archivo está en otra ruta


def generar_token(longitud=8):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(longitud))


def cargar():
    db: Session = SessionLocal()

    try:
        df = pd.read_excel(EXCEL_PATH)

        # Recorre cada columna = un grupo
        for col in df.columns:
            # Toma todos los nombres no vacíos de la columna
            nombres = df[col].dropna().astype(str).str.strip().tolist()

            if not nombres:
                continue

            # El primer nombre de la columna será el nombre del grupo
            nombre_grupo = nombres[0]

            # Crear grupo con token
            grupo = Grupo(
                nombre=nombre_grupo,
                token=generar_token()
            )

            db.add(grupo)
            db.commit()
            db.refresh(grupo)

            # Insertar TODOS los nombres como invitados (incluido el primero)
            for nombre in nombres:
                invitado = Invitado(
                    nombre=nombre,
                    grupo_id=grupo.id
                )
                db.add(invitado)

            db.commit()

        print("✔ Invitados cargados correctamente desde Excel.")

    except Exception as e:
        db.rollback()
        print("❌ Error cargando invitados:", e)

    finally:
        db.close()


if __name__ == "__main__":
    cargar()