from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.models.database import Base

class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True,  index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    dono = relationship("Usuario")
    nome = Column(String, nullable=False)
    descrição = Column(String, nullable=True)
    status = Column(String, nullable=False, default="Pendente")