from django.urls import include, path

urlpatterns = [
    path("api/", include("library.presentors.rest.routers.api.router")),
]
