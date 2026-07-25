from fastapi import FastAPI
from app.models.models.database import engine, Base
from app.models.routes.task_routes import rotas_tarefas
from app.models.routes.user_routes import rotas_user
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(rotas_tarefas)
app.include_router(rotas_user)