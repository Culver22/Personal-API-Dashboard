from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.todo import CreateTodo, ReadTodo
from app.db.models.todo import ToDo
from app.db.database import get_db

router = APIRouter()


# Route to create a new todo and store it in the database
@router.post("/todos", response_model=ReadTodo)
async def create_todo(todo: CreateTodo, db: AsyncSession = Depends(get_db)):
    # Create a new SQLAlchemy todo instance from Pydantic input
    new_todo = ToDo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        completed=todo.completed
    )

    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)  # Refresh in order to get generated fields (e.g. ID)

    return new_todo


@router.get("/todos", response_model=List[ReadTodo])  # Returns a list of todos in the format defined by ReadTodo
async def get_todos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ToDo))  # SELECT * FROM todos
    todos = result.scalars().all()
    return todos


@router.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ToDo).where(ToDo.id == todo_id))
    todo = result.scalars().first()

    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")

    await db.delete(todo)
    await db.commit()
