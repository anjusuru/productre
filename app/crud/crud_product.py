from app.models import Product
from app.schemas import CreateProduct, UpdateProduct

from .base import CRUDBase


class PROCRUD(CRUDBase[Product, CreateProduct, UpdateProduct]):
    pass


product_obj = PROCRUD(Product)
