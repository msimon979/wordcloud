from rest_framework import serializers

from states.models import State


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"

    def update(self, instance: State, validated_data: dict):
        instance.flood_cost_percentage = validated_data.get(
            "flood_cost_percentage", instance.flood_cost_percentage
        )
        instance.monthly_tax = validated_data.get("monthly_tax", instance.monthly_tax)
        instance.save()

        return instance
