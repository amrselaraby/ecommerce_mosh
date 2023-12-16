from ninja import Path, Router
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from .models import Product, Collection, Review
from .schemas import (
    CollectionBase,
    CollectionIn,
    CollectionOut,
    ProductBase,
    ProductIn,
    ReviewBase,
    ReviewIn,
)
from typing import List

router = Router()
review_router = Router(tags=["reviews"])
product_router = Router(tags=["products"])


@product_router.get("/", response=List[ProductBase])
def product_list(request):
    products = Product.objects.select_related("collection").all()
    return products


@product_router.get("/{product_id}", response=ProductBase)
def product_detail(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    return product


@product_router.post("/", response={201: ProductBase})
def product_create(request, payload: ProductIn):
    product = Product.objects.create(**payload.dict())
    # print(payload.dict()["collection"])
    return 201, product


@product_router.put("/{product_id}", response=ProductBase)
def product_update(request, product_id: int, payload: ProductIn):
    product = get_object_or_404(Product, pk=product_id)
    for attr, value in payload.dict().items():
        setattr(product, attr, value)
    product.save()
    return product


@product_router.delete("/{product_id}")
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
def collection_update(request, collection_id: int):
    collection = get_object_or_404(Collection, pk=collection_id)
    if collection.products.count() > 0:
        return {405: "Method Not Allowed"}
    collection.delete()
    return {204: "No Content"}


@review_router.get("/", response=List[ReviewBase])
def reviews_get(request, product_id: int = Path(...)):
    reviews = Review.objects.select_related("product").filter(product_id=product_id)

    return reviews


@review_router.post("/", response={201: ReviewBase})
def review_create(
    request,
    payload: ReviewIn,
    product_id: int = Path(...),
):
    review = Review.objects.create(**payload.dict(), product_id=product_id)
    # print(payload.dict()["collection"])
    return 201, review


@review_router.get("/{review_id}", response=ReviewBase)
def review_detail(request, review_id: int, product_id: int = Path(...)):
    review = get_object_or_404(
        Review.objects.filter(product_id=product_id), pk=review_id
    )
    return review


@review_router.put("/{review_id}", response=ReviewBase)
def review_update(
    request, review_id: int, payload: ReviewIn, product_id: int = Path(...)
):
    review = get_object_or_404(
        Review.objects.filter(product_id=product_id), pk=review_id
    )
    for attr, value in payload.dict().items():
        setattr(review, attr, value)
    review.save()
    return review


@review_router.delete("/{review_id}", response=ReviewBase)
def review_delete(request, review_id: int, product_id: int = Path(...)):
    review = get_object_or_404(
        Review.objects.filter(product_id=product_id), pk=review_id
    )
    review.delete()
    return review


product_router.add_router("{product_id}/reviews", review_router)
router.add_router("/products", product_router)
