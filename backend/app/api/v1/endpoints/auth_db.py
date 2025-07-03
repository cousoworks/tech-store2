from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from jose import jwt

from app.core.security import verify_password, get_password_hash
from app.core.config import settings
from app.db.session import get_session
from app.models.db_models import Usuario, Token

router = APIRouter()

def authenticate_user(db: Session, email: str, password: str) -> Usuario:
    """
    Autenticar un usuario por email y contraseña
    """
    # Buscar el usuario por email
    query = select(Usuario).where(Usuario.email == email)
    result = db.exec(query).first()
    
    if not result:
        return None
    
    if not verify_password(password, result.password_hash):
        return None
    
    return result

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Crear un token de acceso JWT
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    
    return encoded_jwt

@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Obtener token JWT para acceso
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    # Actualizar fecha del último acceso
    user.fecha_ultimo_acceso = datetime.utcnow()
    db.add(user)
    db.commit()
    
    # Crear token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        ),
        "token_type": "bearer"
    }

@router.post("/register", response_model=Token)
def register_user(
    *,
    db: Session = Depends(get_session),
    email: str,
    password: str,
    nombre: str,
    apellidos: str = None
) -> Any:
    """
    Registrar un nuevo usuario
    """
    # Verificar si el correo ya existe
    query = select(Usuario).where(Usuario.email == email)
    user = db.exec(query).first()
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )
    
    # Crear nuevo usuario
    new_user = Usuario(
        email=email,
        nombre=nombre,
        apellidos=apellidos,
        password_hash=get_password_hash(password),
        rol="cliente",
        activo=True,
        fecha_creacion=datetime.utcnow()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Crear token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(
            data={"sub": str(new_user.id)}, expires_delta=access_token_expires
        ),
        "token_type": "bearer"
    }
