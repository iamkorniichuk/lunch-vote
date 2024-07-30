from rest_framework.viewsets import ModelViewSet

from commons.permissions import IsOwnerOrReadOnly
from commons.viewsets import PopulateDataMixin

from .serializers import RestaurantSerializer, MenuSerializer
from .models import Restaurant, Menu


class RestaurantViewSet(PopulateDataMixin, ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

    def get_populated_data(self):
        return {"created_by": self.request.user.pk}

    def get_permissions(self):
        return super().get_permissions() + [IsOwnerOrReadOnly("created_by")]


class MenuViewSet(ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

    def get_permissions(self):
        return super().get_permissions() + [IsOwnerOrReadOnly("restaurant.created_by")]
