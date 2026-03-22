import sys
import os
import pandas as pd
import secrets

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utility.database import SessionLocal
from models.grupo import Grupo
from models.invitado import Invitado

db = SessionLocal()

def generar_token():
    return secrets.token_urlsafe(6)

# leer excel
df = pd.read_excel("invitados.xlsx")

for columna in df.columns:

    invitados = df[columna].dropna().tolist()

    if not invitados:
        continue

    token = generar_token()

    grupo = Grupo(
        nombre_grupo=columna,
        token=token
    )

    db.add(grupo)
    db.commit()
    db.refresh(grupo)

    for nombre in invitados:

        invitado = Invitado(
            nombre=nombre,
            grupo_id=grupo.id
        )

        db.add(invitado)

    db.commit()

    print(f"Grupo creado: {columna} | Token: {token}")