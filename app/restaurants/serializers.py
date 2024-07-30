from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

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
    votes = serializers.SerializerMethodField()

    def get_votes(self, obj):
        return obj.votes.count()


class NestedMenuSerializer(MenuSerializer):
    class Meta:
        model = Menu
        exclude = ["id", "restaurant"]


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"

    menus = NestedMenuSerializer(many=True, read_only=True)
    created_by = RepresentativePkRelatedField(
        queryset=User.objects.all(),
        serializer_class=UserSerializer,
    )
