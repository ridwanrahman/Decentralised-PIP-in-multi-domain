from django.db import models

# Create your models here.

class PredicateKeys(models.Model):
    predicate = models.CharField(max_length=2000, null=True, blank=True)
    predicate_length = models.CharField(max_length=2000, null=True, blank=True)
    tpk = models.TextField(null=True, blank=True)
    apk = models.TextField(null=True, blank=True)
    ask = models.TextField(null=True, blank=True)
    sign = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.predicate

