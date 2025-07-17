from contextlib import asynccontextmanager
from fastapi import FastAPI
from router.todo_router import router as todo_router
from database import create_db_tables
from utils import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await create_db_tables()
    print("Aplicacion iniciada y tablas de DB creadas")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(todo_router)


@app.get("/", tags=["Entrada"])
async def root():
    return {"message": "Api lista de tareas"}
