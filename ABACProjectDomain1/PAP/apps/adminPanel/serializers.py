from rest_framework import serializers
from .models import *

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'resource_name', 'resource_description', 'policy')