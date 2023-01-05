from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from states.models import State
from states.serializers import StateSerializer


class StateDetailView(APIView):
    http_method_names = ["get", "patch", "head", "options"]
    permission_classes = (IsAdminUser,)

    def get(self, request, state_id):
        try:
            state = State.objects.get(id=state_id)
        except State.DoesNotExist:
            return JsonResponse(
                {"error": f"state_id: {state_id} does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = StateSerializer(state)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, state_id):
        try:
            state = State.objects.get(id=state_id)
        except State.DoesNotExist:
            return JsonResponse(
                {"error": f"state_id: {state_id} does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = StateSerializer(instance=state, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
