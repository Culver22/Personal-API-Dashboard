from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.todo import CreateTodo, ReadTodo, UpdateTodo
from app.db.models.todo import ToDo
from app.db.database import get_db

router = APIRouter()


# Route to create a new todo and store it in the database
@router.post("/", response_model=ReadTodo)
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


@router.get("/", response_model=List[ReadTodo])  # Returns a list of todos in the format defined by ReadTodo
async def get_todos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ToDo))  # SELECT * FROM todos
    todos = result.scalars().all()  # Just the Goal objects - ignores row metadata
    return todos


@router.delete("/{todo_id}", status_code=204)  # successfully deleted
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ToDo).where(ToDo.id == todo_id))  # Search for specific todo by ID
    todo = result.scalars().first()

    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")

    await db.delete(todo)
    await db.commit()


@router.patch("/{todo_id}", response_model=ReadTodo)
async def update_todo(todo_id: int, todo_data: UpdateTodo, db: AsyncSession = Depends(get_db)):
    # Load the existing row
    result = await db.execute(select(ToDo).where(ToDo.id == todo_id))
    todo = result.scalars().first()
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")

    # Extract only provided fields
    updates = todo_data.dict(exclude_unset=True) # Exclude any values which are None (Unchanged values)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    # Apply changes to the existing instance (no new row created)
    for key, value in updates.items():
        # protect against accidental id updates
        if key == "id":
            continue
        setattr(todo, key, value)

    await db.commit()
    await db.refresh(todo)
    return todo
