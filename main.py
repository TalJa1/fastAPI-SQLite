from typing import Literal
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from database import get_db, engine, Base
from models.Customer import Customer
from sqlalchemy.orm import Session
from routes import CustomerRoute

# from routes import customerRoute

app = FastAPI(
    title="FastAPI with SQLite",
    description="This is a very fancy project, with auto docs for the API",
    version="0.1.0",
)


# Create the tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Call the function during application startup
@app.on_event("startup")
async def startup_event():
    await init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


app.include_router(CustomerRoute.router, prefix="/api/v1", tags=["Customers"])
