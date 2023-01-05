from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from quotes.helpers import get_quote, update_quote
from quotes.serializers import QuoteSerializer


class QuoteDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "head", "options"]

    def get(self, request, quote_id):
        if quote := get_quote(quote_id):

            if request.user.is_staff is False and quote.user_id != request.user.id:
                return JsonResponse(
                    {
                        "error": f"quote_id: {quote_id} is not associated with user_id: {request.user.id}"
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # If external user and quote is out of date update it
            if request.user.is_staff is False:
                update_quote(quote)
            serializer = QuoteSerializer(quote)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(
            {"error": f"quote_id: {quote_id} does not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )
