import jwt
import os
from datetime import timezone, datetime, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException
load_dotenv()
KEY = os.getenv('JWT_SECRET')
ALGORITMO = 'HS256'
EXPIRA_MIN = 60
def criar_token(user_id: int) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes= EXPIRA_MIN)
    dados = {'sub': str(user_id), 'exp': expira}
    return jwt.encode(dados, KEY, algorithm=ALGORITMO)
def ler_token(token: str) -> int:
    try:
        dados = jwt.decode(token, KEY, algorithms=[ALGORITMO])
        return dados["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Login expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="token Invalido")
