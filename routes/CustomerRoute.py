from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.Customer import (
    Customer as CustomerModel,
    CustomerCreate,
    CustomerRead,
    CustomerUpdate,
)
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

from fastapi import Query


@router.get("/customers/", response_model={}, status_code=200)
async def get_customers(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),  # Offset should be (pagenumber - 1 ) * limit
):
    try:
        # Query database with pagination
        result = await db.execute(select(CustomerModel).offset(offset).limit(limit))
        customers = result.scalars().all()

        if not customers:
            return []

        # Convert to Pydantic models
        response = {
            "message": "Customers retrieved successfully",
            "data": [CustomerRead.model_validate(customer) for customer in customers],
            "limit": limit,
            "offset": offset,
            "total": len(customers),
        }
        logger.info(f"Fetched {len(customers)} customers")
        return response
    except Exception as e:
        # Log the error and re-raise as HTTPException
        print(f"Error retrieving customers: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving customers.")


@router.post("/customers/", response_model=CustomerRead, status_code=201)
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_customer = CustomerModel(**customer.dict())
        db.add(new_customer)
        await db.commit()
        await db.refresh(new_customer)
        return CustomerRead.model_validate(new_customer)
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        raise HTTPException(status_code=500, detail="Error creating customer.")


# Remove customer
@router.delete("/customers/{customer_id}/", response_model=dict, status_code=200)
async def remove_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CustomerModel).filter(CustomerModel.customer_id == customer_id)
    )
    customer = result.scalars().first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    await db.delete(customer)
    await db.commit()

    # Verify if the customer was successfully removed
    result = await db.execute(
        select(CustomerModel).filter(CustomerModel.customer_id == customer_id)
    )
    removed_customer = result.scalars().first()
    if removed_customer:
        return {"message": f"Failed to remove customer with customer id {customer_id}"}

    return {"message": f"Customer removed successfully with customer id {customer_id}"}


# Update customer
@router.put("/customers/{customer_id}/", response_model=dict, status_code=200)
async def update_customer(
    customer_id: int, customer: CustomerUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(CustomerModel).filter(CustomerModel.customer_id == customer_id)
    )
    db_customer = result.scalars().first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in customer.model_dump().items():
        setattr(db_customer, key, value)

    await db.commit()
    await db.refresh(db_customer)

    # Convert SQLAlchemy model instance to Pydantic model instance
    customer_read = CustomerRead.model_validate(db_customer)

    return {
        "message": f"Customer updated successfully with customer id {customer_id}",
        "data": customer_read,
    }


# Get customer by id
@router.get("/customers/{customer_id}/", response_model=CustomerRead, status_code=200)
async def get_customer_by_id(customer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CustomerModel).filter(CustomerModel.customer_id == customer_id)
    )
    customer = result.scalars().first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer
