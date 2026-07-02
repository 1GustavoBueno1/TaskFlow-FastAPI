from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, EmailStr
from app.models.models.database import engine, Base, get_db
import bcrypt
from app.models.models.user_db import Usuario
from app.models.services.auth import criar_token, ler_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
auth2 = OAuth2PasswordBearer(tokenUrl="/usuario/login")

rotas_user = APIRouter(prefix="/usuario", tags=["usuario"])

class Cadastro(BaseModel):
    nome: str
    email: EmailStr
    senha: str
class EditarPerfil(BaseModel):
    nome: str | None
    email: EmailStr | None
    senha: str | None

class UserOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
@rotas_user.post('/cadastro')
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

@rotas_user.post("/login")
def login(dados: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.username).first()
    if not usuario or not bcrypt.checkpw(dados.password.encode(), usuario.senha.encode()):
        raise HTTPException(status_code=401, detail = "Email ou senha invalidos!")
    token = criar_token(usuario.id)

    return {"access_token": token, "token_type": "bearer"}
def usuario_logado(db: Session = Depends(get_db), token: str = Depends(auth2)):
    user_id = ler_token(token)
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario não encontrado")
    return usuario
@rotas_user.get("/perfil")
def ver_perfil(usuario: Usuario = Depends(usuario_logado)):
    return {"id": usuario.id, "nome": usuario.nome, "email": usuario.email}

@rotas_user.put("/editar_perfil", response_model = UserOut)
def editar_perfil(dados: EditarPerfil, usuario: Usuario = Depends(usuario_logado), db: Session = Depends(get_db)):
    campos = dados.model_dump(exclude_unset=True)
    if "email" in campos:
        existe = db.query(Usuario).filter(Usuario.email == campos["email"],Usuario.id != usuario.id).first()
        if existe:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
    if "senha" in campos:
        senha_pura = campos.pop("senha")
        usuario.senha = bcrypt.hashpw(senha_pura.encode(), bcrypt.gensalt()).decode()
    for chave, item in campos.items():
        setattr(usuario, chave, item)

    db.commit()
    db.refresh(usuario)
    return usuario