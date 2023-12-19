from ninja import Field, Schema, ModelSchema, FilterSchema
from decimal import Decimal
from typing import List, Optional
from .models import Collection, Product, Review


class ProductFilterSchema(FilterSchema):
    search: Optional[str] = Field(
        None, q=["title__icontains", "description__icontains"]
    )


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


class ReviewBase(ModelSchema):
    class Meta:
        model = Review
        fields = ["id", "name", "date", "description", "product"]


class ReviewIn(Schema):
    name: str
    description: str
