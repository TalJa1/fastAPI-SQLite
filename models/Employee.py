from datetime import date
from typing import Optional
from sqlalchemy import DECIMAL, Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    position = Column(String(50))
    hire_date = Column(Date)
    salary = Column(DECIMAL(10, 2))


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    position: Optional[str] = None
    hire_date: date
    salary: float


class EmployeeRead(EmployeeBase):
    employee_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        from_attributes = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass
