from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import json
from django.http import JsonResponse



def is_authenticated(request):
    return bool(request.user and request.user.is_authenticated)

def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None
 

class UserCreationView(APIView):
    def post(self, request):
        password = request.data.get("password")
        state = request.data.get("state")

        if password and state:
            context = {"password": password, "state": state}
            serializer = UserSerializer(context=context, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"error": "missing password"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if is_authenticated(request):
            users = self.get_serialized()
            return JsonResponse(data=users, status=status.HTTP_200_OK, safe=False)
        return JsonResponse({"error": "not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    def get_serialized(self):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return serializer.data
        

class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        if user := get_user(user_id):
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return JsonResponse({"error": f"user_id: {user_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, user_id):
        if user := get_user(user_id):
            state = request.data.get("state")
            context = {"state": state}

            serializer = UserSerializer(instance=user, data=request.data, context=context, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
