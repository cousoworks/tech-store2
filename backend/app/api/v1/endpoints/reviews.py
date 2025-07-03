from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.models import Review, ReviewCreate, ReviewRead, User, Product
from app.services.auth import get_current_active_user

router = APIRouter()


@router.get("/product/{product_id}", response_model=List[ReviewRead])
def read_product_reviews(
    *,
    db: Session = Depends(get_session),
    product_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get all reviews for a specific product.
    """
    # First check if the product exists
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    reviews = db.exec(
        select(Review)
        .where(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
    ).all()
    
    return reviews


@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(
    *,
    db: Session = Depends(get_session),
    review_in: ReviewCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new review for a product.
    """
    # Check if product exists
    product = db.get(Product, review_in.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    # Check if user has already reviewed this product
    existing_review = db.exec(
        select(Review)
        .where(Review.product_id == review_in.product_id, Review.user_id == current_user.id)
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product",
        )
    
    # Check if user is trying to review their own product
    if product.seller_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot review your own product",
        )
    
    # Create review
    review = Review(
        **review_in.dict(),
        user_id=current_user.id,
    )
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    return review


@router.get("/{review_id}", response_model=ReviewRead)
def read_review(
    *,
    db: Session = Depends(get_session),
    review_id: int,
) -> Any:
    """
    Get a specific review by ID.
    """
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )
    
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    *,
    db: Session = Depends(get_session),
    review_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a review.
    """
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )
    
    # Check if the user is the author of the review or an admin
    if review.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this review",
        )
    
    db.delete(review)
    db.commit()
    
    return None
