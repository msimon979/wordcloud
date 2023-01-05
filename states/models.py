from django.db import models


# Create your models here.
class State(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint(fields=["state"], name="unique_state")]

    state = models.CharField(max_length=2, null=False)
    flood_cost_percentage = models.DecimalField(max_digits=5, decimal_places=3)
    monthly_tax = models.DecimalField(max_digits=5, decimal_places=3)
