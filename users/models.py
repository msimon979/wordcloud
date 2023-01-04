from django.db import models
from django.conf import settings

# Create your models here.
class UserInformation(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user')
        ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    state = models.CharField(max_length=2, null=False)
    has_pet = models.BooleanField(null=False)
    include_flood_coverage = models.BooleanField(null=False)


    def save(self, *args, **kwargs):
        self.state = self.state.upper()
        super(UserInformation, self).save(*args, **kwargs)