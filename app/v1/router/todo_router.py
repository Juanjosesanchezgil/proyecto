from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from database import get_db, TaskDB


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


router = APIRouter(prefix="/todo", tags=["todo"])


@router.get("/", response_model=List[Task])
async def get_all_tasks(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, description="Numero de tareas a saltar"),
    limit: int = Query(100, description="Numero de tareas a retornar", le=1000),
    completed: Optional[bool] = Query(None, description="Filtra por estado de completado")
):
    query = select(TaskDB)

    if completed is not None:
        query = query.where(TaskDB.completed == completed)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks


@router.get("/{id}", response_model=Task)
async def get_task(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB).filter(TaskDB.id == id))
    task = result.salars().first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def add_task(new_task: TaskCreate, db: AsyncSession = Depends(get_db)):
    db_task = TaskDB(title=new_task.title, description=new_task.description)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


@router.put("/{id}", response_model=Task)
async def update_task(id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB).filter(TaskDB.id == id))
    db_task = result.scalars().first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_task(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB).filter(TaskDB.id == id))
    db_task = result.scalars().first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    await db.delete(db_task)
    await db.commit()
    return
