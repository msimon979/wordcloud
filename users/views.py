from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.helpers import (
    create_user_context,
    get_user,
    is_internal_user,
    patch_user_context,
    user_can_access,
)
from users.serializers import UserSerializer


class UserCreationView(APIView):
    http_method_names = ["get", "post", "head", "options"]

    def post(self, request):
        if context := create_user_context(request):
            serializer = UserSerializer(context=context, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(
            {"error": "missing fields"}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        if is_internal_user(request):
            users = self.get_serialized()
            return JsonResponse(data=users, status=status.HTTP_200_OK, safe=False)
        return JsonResponse(
            {"error": "not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
        )

    def get_serialized(self):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch", "head", "options"]

    def get(self, request, user_id):
        if user_can_access(user_id, request):
            if user := get_user(user_id):
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return JsonResponse(
                {"error": f"user_id: {user_id} does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return JsonResponse(
            {"error": f"user_id: {user_id} does not match request user"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def patch(self, request, user_id):
        if user_can_access(user_id, request):
            if user := get_user(user_id):
                context = patch_user_context(request)

                serializer = UserSerializer(
                    instance=user, data=request.data, context=context, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return JsonResponse(
                {"error": f"user_id: {user_id} does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return JsonResponse(
            {"error": f"user_id: {user_id} can't patch"},
            status=status.HTTP_403_FORBIDDEN,
        )
