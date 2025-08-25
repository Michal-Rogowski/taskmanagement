from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from tasks.api import router as tasks_router
from users.api_auth import router as auth_router
from users.api_users import router as users_router

api = NinjaAPI()
api.add_router("/tasks/", tasks_router)
api.add_router("/auth/", auth_router)
api.add_router("/users/", users_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
]
