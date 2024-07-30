from django.db import models
from django.contrib.auth import get_user_model

from restaurants.models import Menu


User = get_user_model()


class Vote(models.Model):
    class Meta:
        unique_together = ["menu", "user"]

    menu = models.ForeignKey(Menu, models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, models.CASCADE, related_name="votes")

    def __str__(self):
        return f"{self.menu} {self.user.username}"
