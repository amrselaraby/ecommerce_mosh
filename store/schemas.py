from ninja import Schema
from decimal import Decimal
from typing import List
from .models import Collection


class CollectionBase(Schema):
    id: int
    title: str


class ProductBase(Schema):
    id: int
    title: str
    unit_price: Decimal
    unit_price_with_tax: Decimal
    collection: CollectionBase

    @staticmethod
    def resolve_unit_price_with_tax(product):
        return product.unit_price * Decimal(1.1)
