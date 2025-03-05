from django.urls import include, path

urlpatterns = [
    path("v1/", include("library.presentors.rest.routers.api.v1.router")),
]
