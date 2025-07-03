from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.models import Order, OrderCreate, OrderRead, OrderItem, OrderItemCreate, User, Product
from app.services.auth import get_current_active_user, get_current_active_admin

router = APIRouter()


@router.get("/my-orders", response_model=List[OrderRead])
def read_my_orders(
    *,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get all orders for the current user.
    """
    orders = db.exec(
        select(Order)
        .where(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .offset(skip)
        .limit(limit)
    ).all()
    
    return orders


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    *,
    db: Session = Depends(get_session),
    order_items: List[OrderItemCreate],
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new order with items.
    """
    if not order_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No items provided for the order",
        )
    
    # Calculate the total amount and check stock availability
    total_amount = 0.0
    
    for item in order_items:
        product = db.get(Product, item.product_id)
        if not product or not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} not found or not available",
            )
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product {product.name}. Available: {product.stock}",
            )
        
        total_amount += product.price * item.quantity
    
    # Create the order
    order = Order(
        total_amount=total_amount,
        user_id=current_user.id,
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Create the order items and update product stock
    for item_data in order_items:
        product = db.get(Product, item_data.product_id)
        
        # Update product stock
        product.stock -= item_data.quantity
        db.add(product)
        
        # Create order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            price=product.price,
        )
        
        db.add(order_item)
    
    db.commit()
    db.refresh(order)
    
    return order


@router.get("/{order_id}", response_model=OrderRead)
def read_order(
    *,
    db: Session = Depends(get_session),
    order_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific order by ID.
    """
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    
    # Check if the user is the owner of the order or an admin
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this order",
        )
    
    return order


@router.put("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    *,
    db: Session = Depends(get_session),
    order_id: int,
    status: str,
    current_user: User = Depends(get_current_active_admin),
) -> Any:
    """
    Update the status of an order. Only admins can update order status.
    """
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    
    # Validate status
    valid_statuses = ["pending", "paid", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of {', '.join(valid_statuses)}",
        )
    
    # Update status
    order.status = status
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return order


@router.get("/", response_model=List[OrderRead])
def read_orders(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_admin),
) -> Any:
    """
    Get all orders. Only admins can access this endpoint.
    """
    orders = db.exec(
        select(Order)
        .order_by(Order.created_at.desc())
        .offset(skip)
        .limit(limit)
    ).all()
    
    return orders
