from django.conf import settings
from django.db import models

from lib.cost_calculator import CostCalculator

COVERAGE_TYPE_CHOICES = [
    ("basic", "basic"),
    ("premium", "premium"),
]

# Create your models here.
class UserInformation(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user"], name="unique_user")]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    state = models.CharField(max_length=2, null=False)
    has_pet = models.BooleanField(null=False)
    include_flood_coverage = models.BooleanField(null=False)
    coverage_type = models.CharField(
        max_length=20, choices=COVERAGE_TYPE_CHOICES, null=False, default="basic"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.state = self.state.upper()
        super(UserInformation, self).save(*args, **kwargs)

        CostCalculator.create_quote(self)
