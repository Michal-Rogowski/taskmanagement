from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from tasks.api import router as tasks_router

api = NinjaAPI()
api.add_router("/tasks/", tasks_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
]
