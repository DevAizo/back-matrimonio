import secrets

def generar_token():
    return secrets.token_urlsafe(8)