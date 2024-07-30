from django.db import models
from django.contrib.auth import get_user_model

from commons.date import get_current_vote_date


User = get_user_model()


class Restaurant(models.Model):
    name = models.CharField(max_length=64)
    created_by = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return self.name


class Menu(models.Model):
    class Meta:
        unique_together = ["restaurant", "date"]

    restaurant = models.ForeignKey(Restaurant, models.CASCADE, related_name="menus")
    date = models.DateField(default=get_current_vote_date, blank=True)

    def __str__(self):
        return f"{self.restaurant.name} {self.date}"


class Item(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(default="", blank=True)
    menu = models.ForeignKey(Menu, models.CASCADE, related_name="items")

    def __str__(self):
        return self.name
