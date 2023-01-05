# Generated by Django 4.1.4 on 2023-01-05 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="State",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.CharField(max_length=2)),
                (
                    "flood_cost_percentage",
                    models.DecimalField(decimal_places=3, max_digits=5),
                ),
                ("monthly_tax", models.DecimalField(decimal_places=3, max_digits=5)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name="state",
            constraint=models.UniqueConstraint(fields=("state",), name="unique_state"),
        ),
    ]
