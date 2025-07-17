from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.db_engine_session import AsyncSessionLocal
from ..models.pg_db_model import todoCol as ItemModel
from pydantic import BaseModel
from sqlalchemy.future import select

app = FastAPI()

async def get_db():
    async with AsyncSessionLocal() as session: # type: ignore
        yield session

class Item(BaseModel):
    title: str
    desc: str

@app.post("/items/")
async def create_item(item: Item, db: AsyncSession = Depends(get_db)):
    db_item = ItemModel(title=item.title, desc=item.desc)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item