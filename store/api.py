from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from .models import Product, Collection
from .schemas import CollectionBase, CollectionIn, CollectionOut, ProductBase, ProductIn
from typing import List

router = Router()


@router.get("/products", response=List[ProductBase])
def product_list(request):
    products = Product.objects.select_related("collection").all()
    return products


@router.get("/products/{product_id}", response=ProductBase)
def product_detail(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    return product


@router.post("/products/", response={201: ProductBase})
def product_create(request, payload: ProductIn):
    product = Product.objects.create(**payload.dict())
    # print(payload.dict()["collection"])
    return 201, product


@router.put("/products/{product_id}", response=ProductBase)
def product_update(request, product_id: int, payload: ProductIn):
    product = get_object_or_404(Product, pk=product_id)
    for attr, value in payload.dict().items():
        setattr(product, attr, value)
    product.save()
    return product


@router.delete("/products/{product_id}")
def product_update(request, product_id: int, payload: ProductIn):
    product = get_object_or_404(Product, pk=product_id)
    if product.orderitems.count() > 0:
        return {405: "Method Not Allowed"}
    product.delete()
    return {204: "No Content"}


@router.get("/collections/", response=List[CollectionOut])
def collection_list(request):
    collections = Collection.objects.annotate(products_count=Count("products")).all()
    return collections


@router.post("/collections/", response={201: CollectionBase})
def collection_list(request, payload: CollectionIn):
    collection = Collection.objects.create(**payload.dict())
    return collection


@router.get("/collections/{collection_id}", response=CollectionOut)
def collection_list(request, collection_id: int):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count("products")), pk=collection_id
    )
    return collection


@router.put("/collections/{collection_id}", response=CollectionBase)
def collection_update(request, collection_id: int, payload: CollectionIn):
    collection = get_object_or_404(Collection, pk=collection_id)
    for attr, value in payload.dict().items():
        setattr(collection, attr, value)
    collection.save()
    return collection


@router.delete("/collections/{collection_id}")
def product_update(request, collection_id: int):
    collection = get_object_or_404(Collection, pk=collection_id)
    if collection.products.count() > 0:
        return {405: "Method Not Allowed"}
    collection.delete()
    return {204: "No Content"}
