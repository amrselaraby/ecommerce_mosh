from ninja import Schema


class ProductBase(Schema):
    id: int
    title: str
    unit_price: float
