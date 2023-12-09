from ninja import Router
from .models import Product

router = Router()


@router.get("/products/")
def product_list(request):
    return {"hello": "world"}


@router.get("/products/{product_id}")
def product_detail(request, product_id: int):
    return {"product_id": product_id}
