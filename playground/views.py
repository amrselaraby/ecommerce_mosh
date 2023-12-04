from django.shortcuts import render
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, OrderItem, Order, Customer
from ninja import NinjaAPI

app = NinjaAPI()

# Create your views here.


def say_hello(request):
    discounted_price = ExpressionWrapper(
        F("unit_price") * 0.8, output_field=DecimalField()
    )
    result = Product.objects.annotate(dicounted_price=discounted_price)

    return render(request, "hello.html", {"result": list(result)})
