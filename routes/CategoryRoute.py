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


@router.get("/categories/{category_id}", response_model=CategoryRead, status_code=200)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = select(CategoryModel).filter(CategoryModel.category_id == category_id)
        result = await db.execute(query)
        category = result.scalars().first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found.")

        return CategoryRead.model_validate(category)
    except Exception as e:
        print(f"Error retrieving category: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving category.")


@router.post("/categories/", response_model=CategoryRead, status_code=201)
async def create_category(category: CategoryRead, db: AsyncSession = Depends(get_db)):
    try:
        # Check if category already exists
        result = await db.execute(
            select(CategoryModel).filter(
                CategoryModel.category_name == category.category_name
            )
        )
        existing_category = result.scalars().first()

        if existing_category:
            raise HTTPException(
                status_code=400,
                detail=f"Category with name '{category.category_name}' already exists",
            )

        # Create new category
        new_category = CategoryModel(**category.model_dump())
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)

        return CategoryRead.model_validate(new_category)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail="Error creating category.")
