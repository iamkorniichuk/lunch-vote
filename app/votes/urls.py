from django.urls import path

from .views import VoteCreateView, VoteRetrieveView


app_name = "votes"

urlpatterns = [
    path("", VoteRetrieveView.as_view(), name="get"),
    path("<int:pk>/", VoteCreateView.as_view(), name="create"),
]
