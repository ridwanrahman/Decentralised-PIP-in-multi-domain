from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomABACUser(AbstractUser):
    designation = models.CharField(blank=True, max_length=20)
    age = models.CharField(blank=True, max_length=20)
    role = models.CharField(blank=True, max_length=120)
    organization = models.CharField(blank=True, max_length=120)
    suburb = models.CharField(blank=True, max_length=120)
    city = models.CharField(blank=True, max_length=120)
    state = models.CharField(blank=True, max_length=120)
    country = models.CharField(blank=True, max_length=120)

    def __str__(self):
        return self.username