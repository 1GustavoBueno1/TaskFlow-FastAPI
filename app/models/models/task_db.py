from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.models.database import Base

class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True,  index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    dono = relationship("usuario")
    nome = Column(String, nullable=False)
    descrição = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Pendente")