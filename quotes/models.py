from django.db import models

# COVERAGE_TYPE = (
#     ("BASIC", "BASIC"),
#     ("PREMIUM", "PREMIUM"),
# )

# # Create your models here.
# class Quote(models.Model):
#     full_name = models.CharField(max_length=200, null=False)
#     coverage_type = models.CharField(
#         max_length = 20,
#         choices = COVERAGE_TYPE,
#         null=False
#         )
#     state = models.CharField(max_length=2, null=False)
#     has_pet = models.BooleanField(null=False)
#     include_flood_coverage = models.BooleanField(null=False)
#     monthly_subtotal = models.DecimalField(null=False)
#     monthly_taxes = models.DecimalField(null=False)
#     monthly_total = models.DecimalField(null=False)
