from django.urls import include, path

from states.views import StateDetailView

urlpatterns = [
    path("<int:state_id>/", StateDetailView.as_view(), name="state_details"),
]
