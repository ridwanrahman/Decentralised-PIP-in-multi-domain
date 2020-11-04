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

class Policy(models.Model):
    user = models.ForeignKey(CustomABACUser, on_delete=models.CASCADE)
    policy_name = models.CharField(blank=True, null=True, max_length=1000)
    policy_description = models.CharField(blank=True, null=True, max_length=1000)
    policy_version = models.CharField(blank=True, null=True, max_length=1000)
    subject_name = models.CharField(blank=True, null=True, max_length=1000)
    subject_value = models.CharField(blank=True, null=True, max_length=1000)
    action_name = models.CharField(blank=True, null=True, max_length=1000)
    action_value = models.CharField(blank=True, null=True, max_length=1000)
    resource_name = models.CharField(blank=True, null=True, max_length=1000)
    resource_value = models.CharField(blank=True, null=True, max_length=1000)
    environment_name = models.CharField(blank=True, null=True, max_length=1000)
    environment_value = models.CharField(blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.policy_name

# TRUE_FALSE_CHOICES = (
#     (True, 'True'),
#     (False, 'False')
# )


class Resource(models.Model):
    resource_name = models.CharField(blank=True, null=True, max_length=1000)
    access = models.CharField(default="False", max_length=10)
    viewable = models.CharField(default="False", max_length=10)
    policy = models.ForeignKey(Policy, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.resource_name

class ResourceDescription(models.Model):
    resource = models.OneToOneField(Resource, on_delete=models.CASCADE, primary_key=True)
    creator = models.ForeignKey(CustomABACUser, on_delete=models.CASCADE)
    resource_description_1 = models.CharField(blank=True, null=True, max_length=1000)
    resource_description_2 = models.CharField(blank=True, null=True, max_length=1000)
    resource_description_3 = models.CharField(blank=True, null=True, max_length=1000)
    resource_description_4 = models.CharField(blank=True, null=True, max_length=1000)
    resource_description_5 = models.CharField(blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.resource.resource_name