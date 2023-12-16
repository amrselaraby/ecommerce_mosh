from ninja import Schema, ModelSchema
from decimal import Decimal
from typing import List
from .models import Collection, Product


class CollectionBase(ModelSchema):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class CollectionOut(CollectionBase):
    products_count: int


class CollectionIn(Schema):
    title: str


class ProductBase(ModelSchema):
    # id: int
    # title: str
    # unit_price: Decimal

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "unit_price",
        ]

    unit_price_with_tax: Decimal
    collection: CollectionBase

    @staticmethod
    def resolve_unit_price_with_tax(product):
        return product.unit_price * Decimal(1.1)


class ProductIn(Schema):
    title: str
    slug: str
    collection_id: int
    inventory: int
    unit_price: Decimal
