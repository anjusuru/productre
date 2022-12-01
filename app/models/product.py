from app.db.session import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "Product"

    # fields
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    brand = Column(String(20), unique=True)
    price = Column(Float)
    quantity = Column(Integer)
    category = Column(String(30))
