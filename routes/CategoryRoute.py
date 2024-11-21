from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.Category import Category as CategoryModel, CategoryRead

router = APIRouter()


@router.get("/categories/", response_model=list[CategoryRead], status_code=200)
async def get_categories(db: AsyncSession = Depends(get_db)):
    try:
        # Fix: Use CategoryModel in select statement
        query = select(CategoryModel)
        result = await db.execute(query)
        categories = result.scalars().all()

        if not categories:
            return []

        # Convert to Pydantic models
        return [CategoryRead.model_validate(category) for category in categories]
    except Exception as e:
        print(f"Error retrieving categories: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving categories.")
