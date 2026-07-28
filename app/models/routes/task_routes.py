from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, EmailStr
from app.models.models.database import engine, Base, get_db
from app.models.models.user_db import Usuario
from app.models.services.auth import criar_token, ler_token
from app.models.models.task_db import Tasks
from app.models.routes.user_routes import usuario_logado

rotas_tarefas = APIRouter(prefix="/tarefas", tags=["tarefas"])



class CriarTarefa(BaseModel):
    nome: str
    descricao: str | None = None

class SaidaDaTarefa(BaseModel):
    id: int
    nome: str
    descrição: str | None = None
    status: str
    class Config:
        from_attributes = True
class EditarTarefas(BaseModel):
    nome: str | None = None
    descrição: str | None = None
    status: str | None = None

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
    return {'id': nova_tarefa.id, "Nome": nova_tarefa.nome, "Descrição": nova_tarefa.descrição, "Status": nova_tarefa.status}

@rotas_tarefas.get("/visualizar_tarefas", response_model=list[SaidaDaTarefa])
def visualizar_tarefas(usuario: Usuario = Depends(usuario_logado), db: Session = Depends(get_db)):
    return db.query(Tasks).filter(Tasks.user_id == usuario.id).all()

@rotas_tarefas.put("/editar_tarefa/{id_tarefa}", response_model= SaidaDaTarefa)
def editar_tarefas(id_tarefa: int, dados: EditarTarefas, usuario: Usuario = Depends(usuario_logado), db: Session = Depends(get_db)):
    tarefa = db.query(Tasks).filter(Tasks.id == id_tarefa, Tasks.user_id == usuario.id).first()   
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    campos = dados.model_dump(exclude_unset=True)
    for chave, valor in campos.items():
        setattr(tarefa, chave, valor)

    db.commit()
    db.refresh(tarefa)
    return tarefa

@rotas_tarefas.delete("/deletar_tarefa/{id_tarefa}")
def deletar_tarefa(id_tarefa: int, usuario: Usuario = Depends(usuario_logado), db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(Tasks.user_id == usuario.id, id_tarefa == Tasks.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não foi encontrada")
    db.delete(task)
    db.commit()
    return {"Sucesso": "Tarefa deletada"}