from typing import Optional
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr, ConfigDict
from database import Base


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


# Pydantic base model with shared configuration
class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class CustomerCreate(CustomerBase):
    email: EmailStr
    phone: str
    address: str
    city: str
    country: str


class CustomerRead(CustomerBase):
    customer_id: int


class CustomerRemove(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    customer_id: int


class CustomerUpdate(CustomerBase):
    email: EmailStr
    phone: str
    address: str
    city: str
    country: str
