from rest_framework.viewsets import ModelViewSet
from django.db.models import OuterRef, Subquery, Count
from marshmallow.fields import Date

from commons.date import get_current_vote_date
from commons.permissions import IsOwnerOrReadOnly
from commons.viewsets import PopulateDataMixin

from .serializers import RestaurantSerializer, MenuSerializer
from .models import Restaurant, Menu


class RestaurantViewSet(PopulateDataMixin, ModelViewSet):
    serializer_class = RestaurantSerializer

    def get_menu_date(self):
        menu_date = self.request.GET.get("menu_date")
        if menu_date:
            menu_date = Date().deserialize(menu_date)
        return menu_date or get_current_vote_date()

    def get_queryset(self):
        menu_date = self.get_menu_date().isoformat()
        menus = (
            Menu.objects.filter(restaurant=OuterRef("pk"))
            .annotate(votes_count=Count("votes"))
            .order_by()
        )
        return (
            Restaurant.objects.filter(menus__date=menu_date)
            .annotate(votes=Subquery(menus.values("votes_count")))
            .order_by("-votes")
            .all()
        )

    def get_populated_data(self):
        return {"created_by": self.request.user.pk}

    def get_permissions(self):
        return super().get_permissions() + [IsOwnerOrReadOnly("created_by")]


class MenuViewSet(ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

    def get_permissions(self):
        return super().get_permissions() + [IsOwnerOrReadOnly("restaurant.created_by")]
