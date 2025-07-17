from fastapi import APIRouter, Depends
from pydantic import BaseModel
from uuid import uuid4
from app.models.pg_db_model import todoCol  # Use the SQLAlchemy model
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_engine_session import AsyncSessionLocal
from typing import List
from sqlalchemy import select

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session: # type: ignore
        yield session

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoResponse(BaseModel):
    id: str
    title: str
    description: str

@router.post("/create", response_model=TodoResponse)
async def create_item(item: TodoCreate, db: AsyncSession = Depends(get_db)):
    db_item = todoCol(title=item.title, description=item.description)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return TodoResponse(
        id=str(uuid4()),  # Generate a unique ID for the response
        title=str(db_item.title),
        description= str(db_item.description)
    )

@router.get("/todos", response_model=List[TodoResponse])
async def get_todos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(todoCol))
    todos = result.scalars().all()
    return [
        TodoResponse(
            id=str(todo.id),
            title=str(todo.title),
            description=str(todo.description)
        )
        for todo in todos
    ]