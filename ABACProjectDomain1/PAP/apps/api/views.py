from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

# from rest_framework.renderers import JSONRenderer
# from rest_framework_xml.renderers import XMLRenderer
 
from apps.adminPanel.models import *
from apps.api.serializers import *
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes

@api_view(['GET'])
def resource_list(request):
    resources = Resource.objects.filter(viewable=True)
    resource_serializer = ResourceSerializer(resources, many=True)
    return JsonResponse(resource_serializer.data, safe=False, status=status.HTTP_200_OK)

def specific_resource_description(request, name):
    try:
        resource = Resource.objects.get(resource_name = name)
        resource_description = ResourceDescription.objects.get(resource=resource)
        resource_description_serializer = ResourceDescriptionSerializer(resource_description, many=False)
        return JsonResponse(resource_description_serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse({"message":"server error/cannot be found"}, status=status.HTTP_404_NOT_FOUND)
    

def get_specific_resource(request, id):
    try:
        resource = Resource.objects.get(id=id)
        resource_serializer = ResourceSerializer(resource)
        return JsonResponse(resource_serializer.data)
    except Exception:
        return JsonResponse({"message":"resource does not exist"},status=status.HTTP_404_NOT_FOUND)

def policy_list(request):
    policies = Policy.objects.all()
    policy_serializer = PolicySerializer(policies, many=True)
    return JsonResponse(policy_serializer.data, safe=False, status=status.HTTP_200_OK)

def get_specific_policy(request,id):
    try:
        policy = Policy.objects.get(id=id)
        policy_serializer = PolicySerializer(policy)
        return JsonResponse(policy_serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse({"message":"resource does not exist"}, status=status.HTTP_404_NOT_FOUND)

def get_policy_access_structure(request, id):
    try:
        policy = Policy.objects.get(id=id)
        policy_serializer = AccessStructureSerializer(policy)
        return JsonResponse(policy_serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse({"message":"access structure does not exist"}, status=status.HTTP_404_NOT_FOUND)
