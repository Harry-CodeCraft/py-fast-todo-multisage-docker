from fastapi import FastAPI
from app.routers import sample

app = FastAPI()

app.include_router(sample.router)
