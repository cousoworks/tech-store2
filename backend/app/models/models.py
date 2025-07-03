from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: str
    is_active: bool = True
    is_admin: bool = False


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    
    # Relationships
    products: List["Product"] = Relationship(back_populates="seller")
    reviews: List["Review"] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    products: List["Product"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class ProductBase(SQLModel):
    name: str = Field(index=True)
    description: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    is_used: bool = False
    is_active: bool = True
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    seller_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    seller: User = Relationship(back_populates="products")
    category: Category = Relationship(back_populates="products")
    reviews: List["Review"] = Relationship(back_populates="product")
    order_items: List["OrderItem"] = Relationship(back_populates="product")


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None


class ReviewBase(SQLModel):
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")


class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    user: User = Relationship(back_populates="reviews")
    product: Product = Relationship(back_populates="reviews")


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    id: int


class OrderBase(SQLModel):
    total_amount: float
    status: str = "pending"  # pending, paid, shipped, delivered, cancelled
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")


class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    user: User = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int


class OrderItemBase(SQLModel):
    quantity: int = Field(ge=1)
    price: float  # Price at the time of purchase
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")


class OrderItem(OrderItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    order: Order = Relationship(back_populates="items")
    product: Product = Relationship(back_populates="order_items")


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: int


# Token model for authentication
class Token(SQLModel):
    access_token: str
    token_type: str


class TokenPayload(SQLModel):
    sub: Optional[int] = None
