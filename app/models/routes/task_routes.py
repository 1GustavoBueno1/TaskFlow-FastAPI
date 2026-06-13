from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, EmailStr
from app.models.models.database import engine, Base, get_db
import bcrypt
from app.models.models.user_db import Usuario
from app.models.services.auth import criar_token, ler_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.models.task_db import Tasks
from app.models.routes.user_routes import usuario_logado

rotas_tarefas = APIRouter(prefix="/tarefas", tags=["tarefas"])


Base.metadata.create_all(bind = engine)
class CriarTarefa(BaseModel):
    nome: str
    descricao: str
@rotas_tarefas.post("/criar")
def criar_tarefa(tarefa: CriarTarefa, usuario: Usuario = Depends(usuario_logado), db: Session = Depends(get_db)):
    nova_tarefa = Tasks(
        user_id = usuario.id,
        nome = tarefa.nome,
        descrição = tarefa.descricao
    )
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return {"Nome": nova_tarefa.nome, "Descrição": nova_tarefa.descrição, "Status": nova_tarefa.status}