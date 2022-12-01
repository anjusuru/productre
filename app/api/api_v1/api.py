from fastapi import APIRouter

from app.api.api_v1.endpoints import product

router = APIRouter()

router.include_router(product.router, tags=["Product"])
