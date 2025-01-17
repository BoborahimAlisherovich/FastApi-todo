import uvicorn
from fastapi import FastAPI
from .routes import todo_router, index_router
from database.config import engine, Base

import sys
print(sys.path)


app = FastAPI()
app.include_router(todo_router)
app.include_router(index_router)

Base.metadata.create_all(bind=engine) # Databse faylini yaratish. 


if __name__ == "__main__":
    uvicorn.run("todu_app.main:app", port=8000, reload=True)