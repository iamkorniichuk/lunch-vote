from rest_framework import test, status
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Restaurant, Menu

User = get_user_model()


class PermissionTestCase(test.APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.owner = User.objects.create_user(
            username="permission-test-case",
            password="123-test-password",
        )
        cls.restaurant = Restaurant.objects.create(
            name="test-name",
            created_by=cls.owner,
        )
        Menu.objects.create(restaurant=cls.restaurant)
        cls.restaurant_url = reverse(
            "restaurant-detail",
            kwargs={"pk": cls.restaurant.pk},
        )

        cls.not_owner = User.objects.create_user(
            username="permission-test-case-1",
            password="123-test-password",
        )

    def test_update_access_for_owner(self):
        self.client.force_authenticate(self.owner)

        response = self.client.patch(
            self.restaurant_url,
            {"name": "new-test-name"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_access_for_not_owner(self):
        self.client.force_authenticate(self.not_owner)

        response = self.client.patch(
            self.restaurant_url,
            {"name": "new-test-name"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PopulateUserTestCase(test.APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.owner = User.objects.create_user(
            username="populate-user-test-case",
            password="123-test-password",
        )
        cls.restaurant_url = reverse("restaurant-list")

        cls.not_owner = User.objects.create_user(
            username="populate-user-test-case-1",
            password="123-test-password",
        )

    def test_populate_on_null(self):
        self.client.force_authenticate(self.owner)

        response = self.client.post(
            self.restaurant_url,
            {
                "name": "test-name",
            },
            format="json",
        )
        pk = response.json()["id"]
        restaurant = Restaurant.objects.get(pk=pk)
        self.assertEqual(restaurant.created_by.pk, self.owner.pk)

    def test_override_populate(self):
        self.client.force_authenticate(self.owner)

        response = self.client.post(
            self.restaurant_url,
            {
                "name": "test-name",
                "created_by": self.not_owner.pk,
            },
            format="json",
        )
        pk = response.json()["id"]
        restaurant = Restaurant.objects.get(pk=pk)
        self.assertNotEqual(restaurant.created_by.pk, self.not_owner.pk)
