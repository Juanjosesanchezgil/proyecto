from fastapi import FastAPI
from router.todo_router import router as todo_router

app = FastAPI()

app.include_router(todo_router)


@app.get("/", tags=["Entrada"])
async def root():
    return {"message": "Api lista de tareas"}
