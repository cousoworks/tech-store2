from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlmodel import Session, select
import os
from datetime import datetime

from app.db.session import get_session
from app.models.db_models import ArticuloInventario, ArticuloCreate, ArticuloRead, ArticuloUpdate
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=List[ArticuloRead])
def get_articulos(
    skip: int = 0, 
    limit: int = 100,
    nombre: Optional[str] = None,
    db: Session = Depends(get_session)
):
    """
    Obtener lista de productos/artículos.
    """
    query = select(ArticuloInventario)
    
    if nombre:
        query = query.where(ArticuloInventario.nombre.contains(nombre))
    
    articulos = db.exec(query.offset(skip).limit(limit)).all()
    
    # Añadir URLs de imágenes generadas para cada artículo si no tienen
    for articulo in articulos:
        if not articulo.image_url:
            # Generamos URLs de imágenes de Unsplash basadas en el nombre del producto
            query_term = articulo.nombre.split()[0].lower()
            articulo.image_url = f"https://source.unsplash.com/featured/?{query_term}&tech"
    
    return articulos

@router.post("/", response_model=ArticuloRead)
def create_articulo(
    articulo: ArticuloCreate,
    db: Session = Depends(get_session)
):
    """
    Crear un nuevo producto/artículo.
    """
    db_articulo = ArticuloInventario.from_orm(articulo)
    db_articulo.fecha_creacion = datetime.utcnow()
    
    db.add(db_articulo)
    db.commit()
    db.refresh(db_articulo)
    return db_articulo

@router.get("/{articulo_id}", response_model=ArticuloRead)
def get_articulo(
    articulo_id: int,
    db: Session = Depends(get_session)
):
    """
    Obtener un producto/artículo específico por su ID.
    """
    articulo = db.get(ArticuloInventario, articulo_id)
    if not articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    
    if not articulo.image_url:
        # Generamos URL de imagen de Unsplash basada en el nombre del producto
        query_term = articulo.nombre.split()[0].lower()
        articulo.image_url = f"https://source.unsplash.com/featured/?{query_term}&tech"
    
    return articulo

@router.put("/{articulo_id}", response_model=ArticuloRead)
def update_articulo(
    articulo_id: int,
    articulo_update: ArticuloUpdate,
    db: Session = Depends(get_session)
):
    """
    Actualizar un producto/artículo existente.
    """
    db_articulo = db.get(ArticuloInventario, articulo_id)
    if not db_articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    
    articulo_data = articulo_update.dict(exclude_unset=True)
    
    for key, value in articulo_data.items():
        setattr(db_articulo, key, value)
    
    db_articulo.fecha_actualizacion = datetime.utcnow()
    
    db.add(db_articulo)
    db.commit()
    db.refresh(db_articulo)
    return db_articulo

@router.delete("/{articulo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_articulo(
    articulo_id: int,
    db: Session = Depends(get_session)
):
    """
    Eliminar un producto/artículo.
    """
    db_articulo = db.get(ArticuloInventario, articulo_id)
    if not db_articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    
    db.delete(db_articulo)
    db.commit()
    return None

@router.post("/{articulo_id}/upload-image", response_model=ArticuloRead)
async def upload_image(
    articulo_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_session)
):
    """
    Subir una imagen para un producto/artículo.
    """
    db_articulo = db.get(ArticuloInventario, articulo_id)
    if not db_articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    
    # Verificar que sea una imagen
    content_type = file.content_type
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
    
    # Crear directorio si no existe
    upload_dir = os.path.join(settings.STATIC_PATH, settings.UPLOAD_FOLDER)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Guardar la imagen
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"product_{articulo_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{file_ext}"
    file_path = os.path.join(upload_dir, file_name)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Actualizar URL de la imagen
    image_url = f"/static/{settings.UPLOAD_FOLDER}/{file_name}"
    db_articulo.image_url = image_url
    db_articulo.fecha_actualizacion = datetime.utcnow()
    
    db.add(db_articulo)
    db.commit()
    db.refresh(db_articulo)
    
    return db_articulo
