from fastapi import FastAPI
from router.todo_router import router as todo_router
from database import create_db_tables


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_db_tables()

app.include_router(todo_router)


@app.get("/", tags=["Entrada"])
async def root():
    return {"message": "Api lista de tareas"}
