from fastapi import FastAPI
from app.models.models.database import engine, Base
from app.models.routes.task_routes import rotas_tarefas
from app.models.routes.user_routes import rotas_user
app = FastAPI()
Base.metadata.create_all(bind = engine)


app.include_router(rotas_tarefas)
app.include_router(rotas_user)