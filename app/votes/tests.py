from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import timedelta
from rest_framework import test, status

from commons.date import get_current_vote_date
from restaurants.models import Restaurant, Menu


User = get_user_model()


class VotingTestCase(test.APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.owner = User.objects.create_user(
            username="voting-test-case",
            password="123-test-password",
        )
        cls.restaurant = Restaurant.objects.create(
            name="test-name",
            created_by=cls.owner,
        )
        date = get_current_vote_date()
        Menu.objects.create(restaurant=cls.restaurant, date=date.isoformat())
        cls.vote_url = reverse(
            "votes:create",
            kwargs={"pk": cls.restaurant.pk},
        )

        cls.not_owner = User.objects.create_user(
            username="voting-test-case-1",
            password="123-test-password",
        )

    def test_vote_access(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.vote_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.not_owner)
        response = self.client.post(self.vote_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
