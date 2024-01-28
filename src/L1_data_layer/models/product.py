from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id: str
    retailer: str
    product_category: str
    name: str
    unit: str
    unit_price: float
    price: float
    own_brand: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
