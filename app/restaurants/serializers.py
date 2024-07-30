from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from commons.date import get_current_vote_date
from commons.serializers import RepresentativePkRelatedField
from users.serializers import UserSerializer, User

from .models import Restaurant, Menu, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ["menu"]


class MenuSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"

    items = ItemSerializer(many=True)


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"

    menu = serializers.SerializerMethodField()
    created_by = RepresentativePkRelatedField(
        queryset=User.objects.all(),
        serializer_class=UserSerializer,
    )

    def get_menu(self, obj):
        vote_date = get_current_vote_date()
        menu = obj.menus.filter(date=vote_date.isoformat()).first()
        if not menu:
            return None
        serializer = MenuSerializer(menu)
        return serializer.data
