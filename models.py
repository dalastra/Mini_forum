from sqlalchemy import Column, Integer, String, Text
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255))
    resumo = Column(String(255))
    conteudo = Column(Text)
    autor = Column(String(100))