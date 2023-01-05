from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from users.user_service import UserService


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email"]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(self.context["password"])
        user.save()

        UserService.create_user_information(user, self.context)

        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        if password := validated_data.get("password"):
            instance.set_password(password)

        instance.save()

        if state := self.context["state"]:
            UserService.update_user_state(instance, state)

        return instance

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data.update(UserService.get_user_information(instance))
        return data
