import json
import requests
from django.shortcuts import render
from pymongo import MongoClient
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from pymongo import MongoClient
# from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
 
# from apps.adminPanel.models import *
# from apps.api.serializers import *
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def get_all_resources(request):
    r = requests.get('http://localhost:8001/context_handler/api/resources')
    if r.status_code == 200:
        return JsonResponse(r.json(), safe=False)
    else:
        return JsonResponse({"message":"server error/cannot be found"}, status=status.HTTP_404_NOT_FOUND)

def get_resource_description(request, name):
    r = requests.get('http://localhost:8001/context_handler/api/resources/'+name)
    if r.status_code == 200:
        return JsonResponse(r.json(), safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message":"server error/cannot be found"}, status=status.HTTP_404_NOT_FOUND)

def get_policies(request):
    r = requests.get('http://localhost:8001/context_handler/api/policies')
    if r.status_code==200:
        return JsonResponse(r.json(), safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message":"server error/cannot be found"}, status=status.HTTP_404_NOT_FOUND)

def get_specific_policy(request, id):
    r = requests.get('http://localhost:8001/context_handler/api/policies/'+str(id)+'/policy')
    if r.status_code==200:
        return JsonResponse(r.json(), safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message":"server error/cannot be found"}, status=status.HTTP_404_NOT_FOUND)

# @renderer_classes([XMLRenderer])
def get_policy_access_structure(request, id):
    r = requests.get('http://localhost:8001/context_handler/api/policies/'+str(id)+'/access_structure')
    if r.status_code==200:
        return JsonResponse(r.json(), safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message":"server error/cannot be found"}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def sign_verify(request):
    if request.method == 'POST':
        print("i am herererere")
        # print(request.body)
        y = json.loads(request.body)
        tpk = y['tpk']
        apk = y['apk']
        sign = y['sign']
        resource_name = y['resource_name']

        # Find the policy protecting that resource
        mongo_client = MongoClient()
        db = mongo_client.domain1
        col = db.adminPanel_resource

        myquery = {
            "resource_name":resource_name
        }
        doc_resource = col.find_one(myquery)
        policy_id = doc_resource['policy_id']
        myquery = {
            "id":policy_id
        }
        col_policy = db.adminPanel_policy
        doc_policy = col_policy.find_one(myquery)

        subject = doc_policy['subject_value']
        environment = doc_policy['environment_value']
        if subject == None:
            subject = ''
        if environment == None:
            environment = ''
        # print(len(subject))
        # print(len(environment))

        if len(subject) > 0 and len(environment) == 0:
            subject = doc_policy['subject_value'].upper().replace(' ','')
            combined_values = subject
        if len(environment) > 0 and len(subject) == 0:
            environment = doc_policy['environment_value'].upper().replace(' ','')
            combined_values = environment
        elif len(subject) >0 and len(environment) > 0:
            subject = doc_policy['subject_value'].upper().replace(' ','')
            environment = doc_policy['environment_value'].upper().replace(' ','')
            combined_values = subject + ","+environment
        # print(subject)
        # print(environment)
        # combined_values = subject + ","+environment+","+resource_name.upper()+","+"CREATE,READ"
        
        combined_values_list = list(combined_values.split(","))
        print(combined_values_list)
        
        to_send_to_abs = {
            'attributes': combined_values_list,
            'tpk': tpk,
            'apk': apk,
            'sign': sign,
        }
        # print(to_send_to_abs)
        json_object = json.dumps(to_send_to_abs)
        url = 'http://0.0.0.0:8004/'
        x = requests.post(url, data = json_object)
        y = json.loads(x.text)
        print(y['response'])
        
        if y['response'] =='True':
            return JsonResponse({"response":"True"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"response":"False"}, status=status.HTTP_200_OK)
        
    return JsonResponse({"message":"error"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def verify_signature(request):
    if request.method == 'POST':
        # print(request.body)
        y = json.loads(request.body)
        
        # bring in the stored attributes from the database
        mongo_client = MongoClient()
        db = mongo_client.domain1
        col = db.controller_policyattributes
        cursor = list(col.find({}))
        item =cursor[-1]
        attributes = item['attributes'].replace("'","").replace("{","").replace("}","")

        to_send_to_abs = {
            'id': y['api_number'],
            'tpk': y['tpk'],
            'apk': y['apk'],
            'sign': y['sign'],
            'attributes': attributes
        }
        # print("*********")
        print(to_send_to_abs)
        json_object = json.dumps(to_send_to_abs)
        url = 'http://0.0.0.0:8004/verify_signature'
        x = requests.post(url, data = json_object)
        y = json.loads(x.text)
        if y['response'] == 'True':
            return JsonResponse({"response":"True"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"response":"False"}, status=status.HTTP_200_OK)