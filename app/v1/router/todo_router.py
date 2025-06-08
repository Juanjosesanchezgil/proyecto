from fastapi import APIRouter


router = APIRouter(prefix="/todo", tags=["todo"])

todos = []

tarea1 = {
    "id": 1,
    "title": "Tarea 1",
    "description": "Descripcion de la tarea 1",
    "completed": False
}

tarea2 = {
    "id": 2,
    "title": "Tarea 2",
    "description": "Descripcion de la tarea 2",
    "completed": False
}


todos.append(tarea1)
todos.append(tarea2)


@router.get("/")
async def tareas():
    return {"tareas": todos}


@router.get("/id")
async def tarea():
    return {"tarea": tarea}
