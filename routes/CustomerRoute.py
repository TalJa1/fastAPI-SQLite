from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.Customer import (
    Customer as CustomerModel,
    CustomerCreate,
    CustomerRead,
)

router = APIRouter()


@router.get("/customers/", response_model=list[CustomerRead], status_code=200)
async def get_customers(db: AsyncSession = Depends(get_db)):
    try:
        # Query database
        result = await db.execute(select(CustomerModel))
        customers = result.scalars().all()

        if not customers:
            return []

        # Convert to Pydantic models
        return [CustomerRead.model_validate(customer) for customer in customers]
    except Exception as e:
        # Log the error and re-raise as HTTPException
        print(f"Error retrieving customers: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving customers.")
