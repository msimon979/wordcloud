from django.db import models

# Create your models here.


class SubmittedUrls(models.Model):
    submit_datetime_utc = models.DateTimeField(auto_now_add=True)
    url = models.URLField(primary_key=True)
    is_processing = models.BooleanField(default=False)
    processing_start_datetime_utc = models.DateTimeField(null=True)
    is_complete = models.BooleanField(default=False)


class Words(models.Model):
    word = models.CharField(max_length=255, primary_key=True)
    count = models.BigIntegerField()
