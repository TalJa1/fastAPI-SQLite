# models/Category.py
from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from database import Base


# SQLAlchemy model
class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


# Pydantic models
class CategoryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_name: str
    description: Optional[str] = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    category_id: int


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryDelete(CategoryBase):
    message: str
    category_id: int
    status: str = "success"


class CategoryListResponse(CategoryBase):
    pass
