from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.db.session import get_session
from app.models.models import User, UserRead, UserUpdate
from app.services.auth import get_current_active_user, get_current_active_admin

router = APIRouter()


@router.get("/me", response_model=UserRead)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=UserRead)
def update_user_me(
    *,
    db: Session = Depends(get_session),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update current user.
    """
    if user_in.username is not None:
        # Check if username already exists and it's not the current user
        user = db.exec(
            select(User).where(User.username == user_in.username, User.id != current_user.id)
        ).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
    
    if user_in.email is not None:
        # Check if email already exists and it's not the current user
        user = db.exec(
            select(User).where(User.email == user_in.email, User.id != current_user.id)
        ).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    user_data = user_in.dict(exclude_unset=True)
    
    if user_in.password:
        user_data["hashed_password"] = get_password_hash(user_in.password)
        user_data.pop("password", None)
    
    for key, value in user_data.items():
        setattr(current_user, key, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/", response_model=List[UserRead])
def read_users(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_admin),
) -> Any:
    """
    Retrieve users. Only admin users can access this endpoint.
    """
    users = db.exec(select(User).offset(skip).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=UserRead)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_admin),
) -> Any:
    """
    Get a specific user by id. Only admin users can access this endpoint.
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    *,
    db: Session = Depends(get_session),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_admin),
) -> Any:
    """
    Update a user. Only admin users can access this endpoint.
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_data = user_in.dict(exclude_unset=True)
    
    if user_in.password:
        user_data["hashed_password"] = get_password_hash(user_in.password)
        user_data.pop("password", None)
    
    for key, value in user_data.items():
        setattr(user, key, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
