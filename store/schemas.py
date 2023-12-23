from ninja import Field, Schema, ModelSchema, FilterSchema
from decimal import Decimal
from typing import List, Optional
from .models import CartItem, Collection, Product, Review
from uuid import UUID, uuid4


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


class ProductOut(ModelSchema):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


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


class CartItemBase(ModelSchema):
    product: ProductOut
    total_price: Decimal

    class Meta:
        model = CartItem
        fields = ["id", "quantity"]

    @staticmethod
    def resolve_total_price(cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartBase(Schema):
    id: UUID = Field(default_factory=uuid4)


class CartOut(CartBase):
    items: List[CartItemBase]
    total_price: Decimal

    @staticmethod
    def resolve_total_price(cart):
        return sum(
            [item.quantity * item.product.unit_price for item in cart.items.all()]
        )


class CartItemIn(Schema):
    product_id: int = Field(gt=0)
    quantity: int = Field(ge=0)


class MsgError(Schema):
    msg: str
