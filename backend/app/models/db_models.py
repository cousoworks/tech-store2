from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    nombre: str
    apellidos: Optional[str] = None
    password_hash: str
    rol: str
    activo: Optional[bool] = True
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_ultimo_acceso: Optional[datetime] = None
    
    # Relaciones
    pedidos: List["Pedido"] = Relationship(back_populates="usuario")


class ArticuloInventario(SQLModel, table=True):
    __tablename__ = "articulos_inventario"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    nombre: str = Field(index=True)
    descripcion: Optional[str] = None
    cantidad: int
    precio: float
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: Optional[datetime] = None
    
    # Campo para URL de imagen (no existe en la DB original, lo añadiremos en la API)
    image_url: Optional[str] = None
    
    # Relaciones
    pedido_articulos: List["PedidoArticulo"] = Relationship(back_populates="articulo")


class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    usuario_id: int = Field(foreign_key="usuarios.id")
    total: float
    estado: str  # pendiente, pagado, enviado, entregado, cancelado
    fecha_pedido: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: Optional[datetime] = None
    direccion_envio: Optional[str] = None
    notas: Optional[str] = None
    
    # Relaciones
    usuario: Usuario = Relationship(back_populates="pedidos")
    articulos: List["PedidoArticulo"] = Relationship(back_populates="pedido")


class PedidoArticulo(SQLModel, table=True):
    __tablename__ = "pedido_articulos"
    
    pedido_id: int = Field(foreign_key="pedidos.id", primary_key=True)
    articulo_id: int = Field(foreign_key="articulos_inventario.id", primary_key=True)
    cantidad: int
    precio_unitario: float
    
    # Relaciones
    pedido: Pedido = Relationship(back_populates="articulos")
    articulo: ArticuloInventario = Relationship(back_populates="pedido_articulos")


# Modelos para API y respuestas
class UsuarioBase(SQLModel):
    email: str
    nombre: str
    apellidos: Optional[str] = None
    rol: str = "cliente"
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioRead(UsuarioBase):
    id: int
    fecha_creacion: datetime


class UsuarioUpdate(SQLModel):
    email: Optional[str] = None
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    password: Optional[str] = None
    activo: Optional[bool] = None


class ArticuloBase(SQLModel):
    nombre: str
    descripcion: Optional[str] = None
    cantidad: int
    precio: float
    image_url: Optional[str] = None


class ArticuloCreate(ArticuloBase):
    pass


class ArticuloRead(ArticuloBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None


class ArticuloUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    cantidad: Optional[int] = None
    precio: Optional[float] = None
    image_url: Optional[str] = None


class PedidoBase(SQLModel):
    usuario_id: int
    total: float
    estado: str = "pendiente"
    direccion_envio: Optional[str] = None
    notas: Optional[str] = None


class PedidoCreate(PedidoBase):
    pass


class PedidoRead(PedidoBase):
    id: int
    fecha_pedido: datetime
    fecha_actualizacion: Optional[datetime] = None


class PedidoArticuloBase(SQLModel):
    pedido_id: int
    articulo_id: int
    cantidad: int
    precio_unitario: float


class PedidoArticuloCreate(PedidoArticuloBase):
    pass


class PedidoArticuloRead(PedidoArticuloBase):
    pass


# Token model para autenticación
class Token(SQLModel):
    access_token: str
    token_type: str


class TokenPayload(SQLModel):
    sub: Optional[int] = None
