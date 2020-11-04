from django.db import models

# Create your models here.
class PolicyAttributes(models.Model):
    attributes = models.CharField(blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.attributes