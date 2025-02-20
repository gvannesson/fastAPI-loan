from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.endpoints import auth, users, secrets
from app.db.session import engine
from sqlmodel import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="SBA loan prediction app")

app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(secrets.router, prefix="/api")