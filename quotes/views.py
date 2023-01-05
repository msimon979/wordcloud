from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from quotes.models import Quote
from quotes.serializers import QuoteSerializer


def get_quote(quote_id):
    try:
        quote = Quote.objects.get(id=quote_id)
        return quote
    except Quote.DoesNotExist:
        return None


class QuoteDetailView(APIView):
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)
    http_method_names = ["get", "head", "options"]

    def get(self, request, quote_id):
        if quote := get_quote(quote_id):
            serializer = QuoteSerializer(quote)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(
            {"error": f"quote_id: {quote_id} does not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )
