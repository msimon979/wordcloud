from django.urls import path

from quotes.views import QuoteDetailView

urlpatterns = [
    path("<int:quote_id>/", QuoteDetailView.as_view(), name="quote_details"),
]
