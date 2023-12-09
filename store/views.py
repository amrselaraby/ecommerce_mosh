from django.shortcuts import render
from django.http import HttpResponse
from ninja import NinjaAPI

app = NinjaAPI()


@app.get("/")
def product_list(request):
    return {"ok": "ok"}
