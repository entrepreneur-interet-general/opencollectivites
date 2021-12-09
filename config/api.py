from ninja import NinjaAPI
from core.api import router as core_router
from francedata.api import router as fs_router

api = NinjaAPI(version="v1", urls_namespace="api")


api.add_router("/core/", core_router)
api.add_router("/france/", fs_router)
