from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurants.viewsets import RestaurantViewSet, MenuViewSet


router = DefaultRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurant")
router.register("menus", MenuViewSet, basename="menu")

urlpatterns = [
    path("", include(router.urls)),
    path("users/", include("users.urls")),
]
