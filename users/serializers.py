from django.contrib.auth.models import User
from rest_framework import serializers

from quotes.quote_service import QuoteService
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
        if password := self.context.get("password"):
            instance.set_password(password)
            del self.context['password']

        instance.save()

        if self.context:
            UserService.update_user_information(instance, self.context)

        return instance

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data["quotes"] = QuoteService.get_user_quotes(instance.id)
        return data
