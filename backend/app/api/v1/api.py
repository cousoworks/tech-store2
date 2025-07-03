from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, products, categories, reviews, orders
from app.api.v1.endpoints import auth_db, articulos, usuarios, pedidos

api_router = APIRouter()

# Rutas originales (desactivadas por ahora)
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(products.router, prefix="/products", tags=["products"])
# api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
# api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
# api_router.include_router(orders.router, prefix="/orders", tags=["orders"])

# Rutas adaptadas a la base de datos inventario.db
api_router.include_router(auth_db.router, prefix="/auth", tags=["auth"])
api_router.include_router(articulos.router, prefix="/products", tags=["products"])
api_router.include_router(usuarios.router, prefix="/users", tags=["users"])
api_router.include_router(pedidos.router, prefix="/orders", tags=["orders"])
