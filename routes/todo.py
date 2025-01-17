from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from schemas.todo import Todo, TodoCreate, TodoUpdate
from database.config import get_db
from database.orm import TodoDB


router = APIRouter(prefix="/todo", tags=["todo"])

@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED, summary="Create a todo")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    todo = TodoDB.create(db, **todo.model_dump())
    return todo


@router.get("/{todo_id}", response_model=Todo, summary="Get a todo")
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    return TodoDB.get(db, todo_id)


@router.get("/", response_model=List[Todo])
def read_todos(db: Session = Depends(get_db)):
    return TodoDB.all(db)


@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    return TodoDB.update(db, todo_id, **todo.model_dump())


@router.delete("/{todo_id}")
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    todo = TodoDB.delete(db, todo_id)
    if todo:
        return {"message": f"Todo {todo_id} deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)