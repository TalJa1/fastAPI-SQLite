from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr
from typing import Optional

Base = declarative_base()


# SQLAlchemy model
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15))
    address = Column(Text)
    city = Column(String(50))
    country = Column(String(50))


# Pydantic schemas
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr  # Ensure this uses EmailStr for validation
    phone: str
    address: str
    city: str
    country: str


class CustomerRead(CustomerBase):
    customer_id: int

    class Config:
        from_attributes = True


class CustomerRemove(CustomerBase):
    customer_id: int

    class Config:
        from_attributes = True


class CustomerUpdate(CustomerBase):
    first_name: str
    last_name: str
    email: EmailStr  # Ensure this uses EmailStr for validation
    phone: str
    address: str
    city: str
    country: str

    class Config:
        from_attributes = True
