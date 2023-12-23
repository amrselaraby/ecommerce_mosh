from uuid import uuid4
from ninja import Path, Query, Router
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from .models import Cart, CartItem, Product, Collection, Review
from .schemas import (
    CartBase,
    CartItemBase,
    CartItemIn,
    CartOut,
    CollectionBase,
    CollectionIn,
    CollectionOut,
    MsgError,
    ProductBase,
    ProductFilterSchema,
    ProductIn,
    ReviewBase,
    ReviewIn,
)
from typing import List

router = Router()
review_router = Router(tags=["reviews"])
product_router = Router(tags=["products"])
cart_router = Router(tags=["carts"])
cart_item_router = Router(tags=["cart_items"])


@product_router.get("/", response=List[ProductBase])
def product_list(
    request, collection_id: int = None, filters: ProductFilterSchema = Query(...)
):
    products = Product.objects.select_related("collection").all()
    if collection_id:
        products = products.filter(collection_id=collection_id)
    products = filters.filter(products)
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
def product_delete(request, product_id: int, payload: ProductIn):
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
def collection_create(request, payload: CollectionIn):
    collection = Collection.objects.create(**payload.dict())
    return collection


@router.get("/collections/{collection_id}", response=CollectionOut)
def collection_detail(request, collection_id: int):
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
def collection_delete(request, collection_id: int):
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


@cart_router.post("/", response={201: CartBase})
def cart_create(request):
    cart = Cart.objects.create()
    return cart


@cart_router.get("/{uuid:cart_id}", response={200: CartOut})
def cart_details(request, cart_id):
    cart = get_object_or_404(
        Cart.objects.prefetch_related("items__product").all(), pk=cart_id
    )
    return cart


@cart_router.delete("/{uuid:cart_id}", response={204: None})
def cart_delete(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    cart.delete()
    return cart


@cart_item_router.get("/", response=List[CartItemBase])
def cart_items_list(request, cart_id=Path(...)):
    items = (
        CartItem.objects.select_related("cart")
        .select_related("product")
        .filter(cart_id=cart_id)
    )

    return items


@cart_item_router.get("/{item_id}", response=CartItemBase)
def cart_items_details(request, item_id: int, cart_id=Path(...)):
    item = get_object_or_404(
        CartItem.objects.select_related("cart")
        .select_related("product")
        .filter(cart_id=cart_id),
        pk=item_id,
    )

    return item


@cart_item_router.post("/", response={201: CartItemBase, 404: MsgError})
def cart_items_create(request, payload: CartItemIn, cart_id=Path(...)):
    if not Product.objects.filter(pk=payload.product_id).exists():
        return 404, {"msg": "Product does not exist"}
    try:
        item = CartItem.objects.get(cart_id=cart_id, product_id=payload.product_id)
        item.quantity += payload.quantity
        item.save()
    except CartItem.DoesNotExist:
        item = CartItem.objects.create(cart_id=cart_id, **payload.dict())

    return 201, item


@cart_item_router.patch("/", response={200: CartItemBase, 404: MsgError})
def cart_items_update(request, payload: CartItemIn, cart_id=Path(...)):
    if not Product.objects.filter(pk=payload.product_id).exists():
        return 404, {"msg": "Product does not exist"}

    item = CartItem.objects.get(cart_id=cart_id, product_id=payload.product_id)
    item.quantity = payload.quantity
    item.save()

    return 200, item


@cart_item_router.delete("/{item_id}", response={204: None})
def cart_items_delete(request, item_id: int, cart_id=Path(...)):
    item = get_object_or_404(
        CartItem.objects.select_related("cart")
        .select_related("product")
        .filter(cart_id=cart_id),
        pk=item_id,
    )

    item.delete()

    return 204, None


cart_router.add_router("{uuid:cart_id}/items", cart_item_router)
product_router.add_router("{product_id}/reviews", review_router)
router.add_router("/products", product_router)
router.add_router("/carts", cart_router)
