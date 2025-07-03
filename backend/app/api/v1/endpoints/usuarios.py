from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from app.db.session import get_session
from app.models.db_models import Usuario, UsuarioCreate, UsuarioRead, UsuarioUpdate
from app.core.security import get_password_hash, verify_password
from app.api.v1.deps import get_current_user, get_current_admin_user

router = APIRouter()

@router.get("/", response_model=List[UsuarioRead])
def get_usuarios(
    skip: int = 0,
    limit: int = 100,
    nombre: Optional[str] = None,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin_user)
):
    """
    Obtener lista de usuarios. Solo disponible para administradores.
    """
    query = select(Usuario)
    
    if nombre:
        query = query.where(Usuario.nombre.contains(nombre) | Usuario.apellidos.contains(nombre))
    
    usuarios = db.exec(query.offset(skip).limit(limit)).all()
    return usuarios

@router.get("/me", response_model=UsuarioRead)
def get_user_me(current_user: Usuario = Depends(get_current_user)):
    """
    Obtener los datos del usuario actualmente autenticado
    """
    return current_user

@router.get("/{usuario_id}", response_model=UsuarioRead)
def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener un usuario específico por su ID.
    """
    # Verificar permisos (solo el propio usuario o administrador)
    if current_user.id != usuario_id and current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a estos datos"
        )
    
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario

@router.put("/me", response_model=UsuarioRead)
def update_user_me(
    *,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualizar los datos del usuario actual
    """
    usuario_data = usuario_update.dict(exclude_unset=True)
    
    # Si se proporciona contraseña, actualizarla
    if "password" in usuario_data:
        usuario_data["password_hash"] = get_password_hash(usuario_data["password"])
        del usuario_data["password"]
    
    # No permitir cambiar el rol desde aquí
    if "rol" in usuario_data:
        del usuario_data["rol"]
    
    for key, value in usuario_data.items():
        setattr(current_user, key, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.put("/{usuario_id}", response_model=UsuarioRead)
def update_usuario(
    *,
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin_user)
):
    """
    Actualizar los datos de un usuario. Solo disponible para administradores.
    """
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario_data = usuario_update.dict(exclude_unset=True)
    
    # Si se proporciona contraseña, actualizarla
    if "password" in usuario_data:
        usuario_data["password_hash"] = get_password_hash(usuario_data["password"])
        del usuario_data["password"]
    
    for key, value in usuario_data.items():
        setattr(usuario, key, value)
    
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    
    return usuario

@router.delete("/{usuario_id}", response_model=UsuarioRead)
def delete_usuario(
    *,
    usuario_id: int,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_admin_user)
):
    """
    Eliminar un usuario. Solo disponible para administradores.
    """
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # No permitir eliminar al propio administrador
    if usuario_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puede eliminar su propia cuenta"
        )
    
    db.delete(usuario)
    db.commit()
    
    return usuario
