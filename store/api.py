from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Product
from .schema import ProductBase
from typing import List

router = Router()


@router.get("/products/", response=List[ProductBase])
def product_list(request):
    products = Product.objects.all()
    return products


@router.get("/products/{product_id}", response=ProductBase)
def product_detail(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    return product
