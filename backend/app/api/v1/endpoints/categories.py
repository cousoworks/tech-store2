from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.models import Category, CategoryCreate, CategoryRead
from app.services.auth import get_current_active_admin

router = APIRouter()


@router.get("/", response_model=List[CategoryRead])
def read_categories(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve categories.
    """
    categories = db.exec(select(Category).offset(skip).limit(limit)).all()
    return categories


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    *,
    db: Session = Depends(get_session),
    category_in: CategoryCreate,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Create new category. Only admin users can create categories.
    """
    # Check if category with this name already exists
    db_category = db.exec(select(Category).where(Category.name == category_in.name)).first()
    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A category with this name already exists",
        )
    
    category = Category.from_orm(category_in)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/{category_id}", response_model=CategoryRead)
def read_category(
    *,
    db: Session = Depends(get_session),
    category_id: int,
) -> Any:
    """
    Get category by ID.
    """
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    *,
    db: Session = Depends(get_session),
    category_id: int,
    category_in: CategoryCreate,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Update a category. Only admin users can update categories.
    """
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    # Check if name already exists and it's not the current category
    if category_in.name != category.name:
        existing = db.exec(
            select(Category).where(Category.name == category_in.name)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A category with this name already exists",
            )
    
    category_data = category_in.dict()
    for key, value in category_data.items():
        setattr(category, key, value)
    
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    *,
    db: Session = Depends(get_session),
    category_id: int,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Delete a category. Only admin users can delete categories.
    """
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    db.delete(category)
    db.commit()
    return None
