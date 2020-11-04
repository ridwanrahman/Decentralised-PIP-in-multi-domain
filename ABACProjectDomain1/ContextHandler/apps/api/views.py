import requests

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

# from rest_framework.renderers import JSONRenderer
# from rest_framework_xml.renderers import XMLRenderer
 
# from apps.adminPanel.models import *
# from apps.api.serializers import *
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes


def get_all_resources(request):
    r = requests.get('http://localhost:8003/pap/api/resources/')
    if r.status_code == 200:
        return JsonResponse(r.json(), safe=False)
    else:
        return JsonResponse({"message":"server error/cannot be found"}, status=status.HTTP_404_NOT_FOUND)

def get_resource_description(request, name):
    r = requests.get('http://localhost:8003/pap/api/resources/'+name)
    if r.status_code == 200:
        return JsonResponse(r.json(), safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message":"server error/cannot be found"}, status=status.HTTP_404_NOT_FOUND)

def get_policies(request):
    r = requests.get('http://localhost:8003/pap/api/policies')
    if r.status_code==200:
        return JsonResponse(r.json(), safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message":"server error/cannot be found"}, status=status.HTTP_404_NOT_FOUND)

def get_specific_policy(request, id):
    r = requests.get('http://localhost:8003/pap/api/policies/'+str(id)+'/policy')
    if r.status_code==200:
        return JsonResponse(r.json(), safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message":"server error/cannot be found"}, status=status.HTTP_404_NOT_FOUND)

def get_policy_access_structure(request, id):
    r = requests.get('http://localhost:8003/pap/api/policies/'+str(id)+'/access_structure')
    if r.status_code==200:
        return JsonResponse(r.json(), safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message":"server error/cannot be found"}, status=status.HTTP_404_NOT_FOUND)