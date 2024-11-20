from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.Customer import (
    Customer as CustomerModel,
    CustomerUpdate,
    CustomerCreate,
    CustomerRead,
)

router = APIRouter()


@router.get("/customers/", response_model=list[CustomerRead], status_code=200)
async def get_customers(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(CustomerModel))
        customers = result.scalars().all()
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
