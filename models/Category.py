from sqlalchemy import Column, Integer, String
from database import Base


class Category(Base):
    __tablename__ = "categories"

    catergory_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), nullable=False)
    description = Column(String(200))


class CategoryBase(Base):
    category_name: str
    description: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    category_id: int


class CategoryRemove(Base):
    category_id: int


class CategoryUpdate(CategoryBase):
    pass
