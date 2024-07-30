from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(
            username=self.model.normalize_username(username), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields["is_superuser"] = True
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
    )

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.get_username()
