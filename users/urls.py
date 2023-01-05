from django.urls import path

from users.views import UserCreationView, UserDetailView

urlpatterns = [
    path("", UserCreationView.as_view(), name="users"),
    path("<int:user_id>/", UserDetailView.as_view(), name="user_details"),
]
