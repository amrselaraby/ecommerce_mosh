from ninja import NinjaAPI
from store.api import router as store_router

api = NinjaAPI(csrf=False)

api.add_router("/store/", store_router, tags=["store"])
