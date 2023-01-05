from django.db import models


class Quote(models.Model):
    class Meta:
        unique_together = (
            "user_id",
            "coverage_type",
            "state",
            "has_pet",
            "include_flood_coverage",
        )

    full_name = models.CharField(max_length=200, null=False)
    coverage_type = models.CharField(max_length=20, null=False)
    state = models.CharField(max_length=2, null=False)
    has_pet = models.BooleanField(null=False)
    include_flood_coverage = models.BooleanField(null=False)
    monthly_subtotal = models.FloatField(null=False)
    monthly_taxes = models.FloatField(null=False)
    monthly_total = models.FloatField(null=False)
    user_id = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
