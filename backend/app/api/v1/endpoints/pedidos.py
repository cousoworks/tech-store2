from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from app.db.session import get_session
from app.models.db_models import (
    Pedido, PedidoCreate, PedidoRead, 
    PedidoArticulo, PedidoArticuloCreate,
    ArticuloInventario
)
from app.api.v1.deps import get_current_user
from app.models.db_models import Usuario

router = APIRouter()

@router.post("/", response_model=PedidoRead)
def create_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crear un nuevo pedido.
    """
    # Verificar que el usuario existe
    if pedido.usuario_id != current_user.id and current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para crear pedidos para otros usuarios"
        )
    
    # Crear el pedido
    db_pedido = Pedido.from_orm(pedido)
    db_pedido.fecha_pedido = datetime.utcnow()
    
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    
    return db_pedido

@router.get("/", response_model=List[PedidoRead])
def get_pedidos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener lista de pedidos. Si es admin, puede ver todos. Si es cliente, solo ve los suyos.
    """
    query = select(Pedido)
    
    # Si no es admin, filtrar solo los pedidos del usuario
    if current_user.rol != "admin":
        query = query.where(Pedido.usuario_id == current_user.id)
    
    pedidos = db.exec(query.offset(skip).limit(limit)).all()
    return pedidos

@router.get("/{pedido_id}", response_model=PedidoRead)
def get_pedido(
    pedido_id: int,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener un pedido específico por su ID.
    """
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Verificar permisos
    if current_user.rol != "admin" and pedido.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver este pedido"
        )
    
    return pedido

@router.post("/{pedido_id}/articulos", response_model=PedidoArticuloCreate)
def add_articulo_to_pedido(
    pedido_id: int,
    pedido_articulo: PedidoArticuloCreate,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Añadir un artículo a un pedido existente.
    """
    # Verificar que el pedido existe
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Verificar permisos
    if current_user.rol != "admin" and pedido.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para modificar este pedido"
        )
    
    # Verificar que el artículo existe
    articulo = db.get(ArticuloInventario, pedido_articulo.articulo_id)
    if not articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    
    # Verificar stock disponible
    if articulo.cantidad < pedido_articulo.cantidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock insuficiente. Disponible: {articulo.cantidad}"
        )
    
    # Crear la relación pedido-artículo
    db_pedido_articulo = PedidoArticulo.from_orm(pedido_articulo)
    
    # Actualizar stock
    articulo.cantidad -= pedido_articulo.cantidad
    
    # Actualizar el total del pedido
    pedido.total += pedido_articulo.cantidad * pedido_articulo.precio_unitario
    pedido.fecha_actualizacion = datetime.utcnow()
    
    db.add(db_pedido_articulo)
    db.commit()
    
    return pedido_articulo

@router.put("/{pedido_id}/estado", response_model=PedidoRead)
def update_pedido_estado(
    pedido_id: int,
    estado: str,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualizar el estado de un pedido.
    """
    # Verificar que el pedido existe
    pedido = db.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Solo admin puede cambiar estados (excepto a cancelado que también puede el dueño)
    if current_user.rol != "admin" and (pedido.usuario_id != current_user.id or estado != "cancelado"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para cambiar el estado de este pedido"
        )
    
    # Validar estado
    estados_validos = ["pendiente", "pagado", "enviado", "entregado", "cancelado"]
    if estado not in estados_validos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estado no válido. Valores permitidos: {', '.join(estados_validos)}"
        )
    
    pedido.estado = estado
    pedido.fecha_actualizacion = datetime.utcnow()
    
    db.commit()
    db.refresh(pedido)
    
    return pedido
