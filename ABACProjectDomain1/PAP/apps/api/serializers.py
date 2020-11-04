from rest_framework import serializers
from apps.adminPanel.models import *

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('__all__')

class ResourceDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceDescription
        fields = ('__all__')

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('id','policy_name','policy_description','subject_value','action_value','resource_value','environment_value')

class AccessStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('id','subject_name','action_name','resource_name','environment_name')