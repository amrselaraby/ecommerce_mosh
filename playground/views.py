from django.shortcuts import render
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, OrderItem, Order
from ninja import NinjaAPI

app = NinjaAPI()

# Create your views here.


def say_hello(request):
    query_set = (
        Order.objects.select_related("customer")
        .prefetch_related("orderitem_set__product")
        .order_by(
            "-placed_at",
        )[:5]
    )

    return render(request, "hello.html", {"query_set": list(query_set)})
