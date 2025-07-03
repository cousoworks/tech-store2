from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from sqlmodel import Session, select, or_

from app.db.session import get_session
from app.models.models import Product, ProductCreate, ProductRead, ProductUpdate, User
from app.services.auth import get_current_active_user
from app.services.file_upload import save_upload_file, delete_file

router = APIRouter()


@router.get("/", response_model=List[ProductRead])
def read_products(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_used: Optional[bool] = None,
    sort_by: str = "created_at",
    sort_desc: bool = True
) -> Any:
    """
    Retrieve products with filtering and sorting options.
    """
    query = select(Product).where(Product.is_active == True)
    
    # Apply filters if provided
    if category_id:
        query = query.where(Product.category_id == category_id)
    
    if search:
        query = query.where(
            or_(
                Product.name.contains(search),
                Product.description.contains(search)
            )
        )
    
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    
    if is_used is not None:
        query = query.where(Product.is_used == is_used)
    
    # Apply sorting
    if sort_desc:
        query = query.order_by(getattr(Product, sort_by).desc())
    else:
        query = query.order_by(getattr(Product, sort_by))
    
    products = db.exec(query.offset(skip).limit(limit)).all()
    return products


@router.get("/popular", response_model=List[ProductRead])
def read_popular_products(
    *,
    db: Session = Depends(get_session),
    limit: int = 10
) -> Any:
    """
    Get popular products (this is a simplified version without reviews count).
    In a production system, you might want to add logic for sorting by average review score.
    """
    products = db.exec(
        select(Product)
        .where(Product.is_active == True)
        .order_by(Product.created_at.desc())
        .limit(limit)
    ).all()
    return products


@router.get("/new", response_model=List[ProductRead])
def read_new_products(
    *,
    db: Session = Depends(get_session),
    limit: int = 10
) -> Any:
    """
    Get newest products.
    """
    products = db.exec(
        select(Product)
        .where(Product.is_active == True)
        .order_by(Product.created_at.desc())
        .limit(limit)
    ).all()
    return products


@router.get("/my-products", response_model=List[ProductRead])
def read_my_products(
    *,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get products for the current user.
    """
    products = db.exec(
        select(Product)
        .where(Product.seller_id == current_user.id)
        .order_by(Product.created_at.desc())
    ).all()
    return products


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    *,
    db: Session = Depends(get_session),
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    is_used: bool = Form(False),
    category_id: int = Form(...),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new product.
    """
    # Handle image upload if provided
    image_url = None
    if image:
        image_url = await save_upload_file(image, "products")
    
    # Create product
    product_data = {
        "name": name,
        "description": description,
        "price": price,
        "stock": stock,
        "is_used": is_used,
        "category_id": category_id,
        "image_url": image_url,
        "seller_id": current_user.id
    }
    
    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductRead)
def read_product(
    *,
    db: Session = Depends(get_session),
    product_id: int,
) -> Any:
    """
    Get product by ID.
    """
    product = db.get(Product, product_id)
    if not product or not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    *,
    db: Session = Depends(get_session),
    product_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    stock: Optional[int] = Form(None),
    is_active: Optional[bool] = Form(None),
    category_id: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a product.
    """
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    # Check if the current user is the seller or an admin
    if product.seller_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this product",
        )
    
    # Update fields if provided
    if name is not None:
        product.name = name
    
    if description is not None:
        product.description = description
    
    if price is not None:
        product.price = price
    
    if stock is not None:
        product.stock = stock
    
    if is_active is not None:
        product.is_active = is_active
    
    if category_id is not None:
        product.category_id = category_id
    
    # Handle image upload if provided
    if image:
        # Delete old image if exists
        if product.image_url:
            delete_file(product.image_url)
        
        # Save new image
        product.image_url = await save_upload_file(image, "products")
    
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    *,
    db: Session = Depends(get_session),
    product_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a product (soft delete by setting is_active = False).
    """
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    # Check if the current user is the seller or an admin
    if product.seller_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this product",
        )
    
    # Soft delete
    product.is_active = False
    db.add(product)
    db.commit()
    
    return None
