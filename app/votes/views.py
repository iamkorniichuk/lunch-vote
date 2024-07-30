from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404

from commons.date import get_current_vote_date
from restaurants.models import Restaurant

from .models import Vote


class VoteRetrieveView(APIView):
    def get(self, request):
        user = request.user
        vote = get_list_or_404(
            Vote, user=user, menu__date=get_current_vote_date().isoformat()
        )[0]
        restaurant = vote.menu.restaurant
        return Response(
            {"detail": f"You've voted for {restaurant.name}"},
            status=status.HTTP_200_OK,
        )


class VoteCreateView(APIView):
    def post(self, request, pk):
        user = request.user
        restaurant = get_object_or_404(Restaurant, pk=pk)
        created_by = restaurant.created_by

        if created_by == user:
            return Response(
                {"detail": f"You can't vote for your restaurant"},
                status=status.HTTP_403_FORBIDDEN,
            )

        menu = get_list_or_404(
            restaurant.menus, date=get_current_vote_date().isoformat()
        )[0]

        Vote.objects.update_or_create(
            user=user,
            defaults={"menu": menu},
        )
        return Response(
            {"detail": f"You've voted for {restaurant.name}"},
            status=status.HTTP_201_CREATED,
        )
