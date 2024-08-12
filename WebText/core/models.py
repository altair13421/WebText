from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class NameModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

class BaseModel(TimeStampedModel, NameModel):
    class Meta:
        abstract = True
