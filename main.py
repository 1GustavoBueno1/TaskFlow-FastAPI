from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from app.models.models.database import engine, Base, get_db
import bcrypt
from app.models.models.user_db import Usuario
from app.models.services.auth import criar_token, ler_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
app = FastAPI()
auth2 = OAuth2PasswordBearer(tokenUrl="auth/login")
Base.metadata.create_all(bind = engine)

@app.get("/")
def route():
    return {"hello": "word"}

class Cadastro(BaseModel):
    nome: str
    email: EmailStr
    senha: str
@app.post('/auth/cadastro')
def cadastrar(usuario : Cadastro, db: Session = Depends(get_db)):
    email_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if email_existente:
        raise HTTPException(status_code = 400, detail="Email ja cadastrado")
    senha_hash = bcrypt.hashpw(usuario.senha.encode(), bcrypt.gensalt())
    novo_user = Usuario(
        nome = usuario.nome,
        email = usuario.email,
        senha = senha_hash.decode()
    )
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    return {"Nome recebido": usuario.nome, "email": usuario.email}

@app.post("/auth/login")
def login(dados: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario or not bcrypt.checkpw(dados.senha.encode(), usuario.senha.encode()):
        raise HTTPException(status_code=401, detail = "Email ou senha invalidos!")
    token = criar_token(usuario.id)

    return {"access_token": token, "token_type": "bearer"}
def usuario_logado(db: Session = Depends(get_db), token: str = Depends(auth2)):
    user_id = ler_token(token)
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario não encontrado")
    return usuario