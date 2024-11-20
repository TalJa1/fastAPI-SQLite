from typing import List, Literal
from uuid import uuid4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from routes import customerRoute

app = FastAPI(
    title="FastAPI with SQLite",
    description="This is a very fancy project, with auto docs for the API",
    version="0.1.0",
)
# handler = Mangum(app)  # for AWS Lambda


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


app.include_router(customerRoute.router, prefix="/api/v1", tags=["Customers"])
