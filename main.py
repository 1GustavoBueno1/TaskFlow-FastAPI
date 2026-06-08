from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from app.models.database import engine, Base, get_db
import bcrypt
from app.models.user_db import Usuario


app = FastAPI()

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