from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
 
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes

# GET all resources

def get_all_resources(request):
    resources = Resource.objects.all()
    resource_serializer = ResourceSerializer(resources, many=True)

    return JsonResponse(resource_serializer.data)

# GET all policies

# GET specific resource

# GET specific policy
