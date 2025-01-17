from sqlalchemy import Column, Integer, String,Boolean
from .config import Base


class Todo(Base):
    __tablename__ = "todo"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, index=True)
    description: str = Column(String, nullable=True)
    done =Column(Boolean, default=False)
