from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.Category import (
    Category as CategoryModel,
    CategoryCreate,
    CategoryListResponse,
    CategoryRead,
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


# routes/CategoryRoute.py
@router.get("/categories/", response_model=list[CategoryRead], status_code=200)
async def get_categories(db: AsyncSession = Depends(get_db)):
    try:
        query = select(CategoryModel)
        result = await db.execute(query)
        categories = result.scalars().all()

        if not categories:
            return []

        # Convert to dict and exclude ID
        # return [
        #     CategoryListResponse(
        #         category_name=category.category_name, description=category.description
        #     )
        #     for category in categories
        # ]

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
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Check if category already exists
        result = await db.execute(
            select(CategoryModel).filter(
                CategoryModel.category_name == category.category_name
            )
        )
        existing_category = result.scalars().first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category already exists.")

        new_category = CategoryModel(**category.dict())
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)
        return CategoryRead.model_validate(new_category)
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail="Error creating category.")


@router.put("/categories/{category_id}", response_model=CategoryRead, status_code=200)
async def update_category(
    category_id: int, category: CategoryRead, db: AsyncSession = Depends(get_db)
):
    try:
        # Check if category exists
        query = select(CategoryModel).filter(CategoryModel.category_id == category_id)
        result = await db.execute(query)
        existing_category = result.scalars().first()

        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found.")

        # Check if new category name already exists (excluding current category)
        name_check = await db.execute(
            select(CategoryModel).filter(
                CategoryModel.category_name == category.category_name,
                CategoryModel.category_id != category_id,
            )
        )
        duplicate_name = name_check.scalars().first()

        if duplicate_name:
            raise HTTPException(
                status_code=400,
                detail=f"Category with name '{category.category_name}' already exists",
            )

        # Update category
        for key, value in category.model_dump(exclude_unset=True).items():
            setattr(existing_category, key, value)

        await db.commit()
        await db.refresh(existing_category)

        return CategoryRead.model_validate(existing_category)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating category: {e}")
        raise HTTPException(status_code=500, detail="Error updating category.")


@router.delete("/categories/{category_id}", response_model={}, status_code=200)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Check if category exists
        query = select(CategoryModel).filter(CategoryModel.category_id == category_id)
        result = await db.execute(query)
        existing_category = result.scalars().first()

        if not existing_category:
            raise HTTPException(status_code=404, detail="Category not found.")

        # Delete with proper async session management
        await db.delete(existing_category)

        # Commit the transaction
        try:
            await db.commit()
        except Exception as commit_error:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to commit delete operation: {str(commit_error)}",
            )

        # Verify deletion
        verify_query = select(CategoryModel).filter(
            CategoryModel.category_id == category_id
        )
        verify_result = await db.execute(verify_query)
        if verify_result.scalars().first():
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Failed to delete category - still exists after deletion",
            )

        return {"message": "Category deleted successfully", "category_id": category_id}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print(f"Error deleting category: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error deleting category: {str(e)}"
        )
