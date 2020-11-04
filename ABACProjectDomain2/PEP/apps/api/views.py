import requests
import json
import time

from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from .models import *
from PEP import variables
from apps.home.models import *

@csrf_exempt
def get_access_structure(request):
    if request.method == 'POST':
        print(request.POST.get('resource_name'))
        r = requests.get('http://localhost:8000/pep/api/policies/'+request.POST.get('resource_name')+'/access_structure')
        if r.status_code == 200:
            variables.access_structure = r.json()
        return JsonResponse(r.json(), safe=False, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message":"view working"})

def Convert(string): 
    li = list(string.split(",")) 
    return li

@csrf_exempt
def generate_signature(request):
    print("generate sig button cliekc")
    if(request.method=='POST'):
        print("****")
        print(request.POST)

        data = request.POST.__getitem__("data")
        # print(data)
        
        # GET RESOURCE NAME
        resource_name = request.POST.__getitem__("resource_name")
        print(resource_name)

        to_send = {
            'user':request.user.email,
            'attributes':data
        }
        
        # #call PIP for attrbutes of user which is runnning on 9001 port
        # print("calliing PIP ")
        r = requests.post('http://localhost:9001/pip/api/get_user_attributes', data=to_send)
        if r.status_code == 404:
            print("hererererere")
            print("got 404")
            print(r.json())
            return JsonResponse(r.json(), safe=False, status=status.HTTP_200_OK)
        if r.status_code == 200:
            print("herere")
            # print(r.json())
            attributes = r.json()
            # print(attributes['attributes'])
            to_send_to_abs = {
                'attributes': attributes['attributes']
            }
            print("hhhhh")
            # print(type(to_send_to_abs))
            json_object = json.dumps(to_send_to_abs)
            # print(json_object)
            url = 'http://0.0.0.0:9004/'
            x = requests.post(url, data = json_object)

            y = json.loads(x.text)
            print("this is the thing i am sending to domain1")

            to_send_to_domain1 = {
                'tpk': y['tpk'],
                'apk': y['apk'],
                'sign': y['sign'],
                'resource_name': resource_name
            }
            json_object = json.dumps(to_send_to_domain1)
            # print(to_send_to_domain1)

            url = 'http://localhost:8000/pep/api/sign_verify'
            x = requests.post(url, data = json_object)
            print(x.text)
            y = json.loads(x.text)
            if y['response'] == 'True':
                return JsonResponse({"response":"True"})
            else:
                return JsonResponse({"response":"False"})

@csrf_exempt
def playground_generate_signature(request):
    if request.method == 'POST':
        # print(request.POST)
        predicate = request.POST.__getitem__("predicate")
        print(predicate)

        #get api countet
        mongo_client = MongoClient()
        db = mongo_client.domain2
        col = db.api_hit_counter
        cursor = list(col.find({}))
        item =cursor[-1]
        id = item['id']
        id = int(id)
        myquery = { "id": id }
        id = id + 1
        print(id)
        newvalues = { "$set": { "id": id }}
        col.update_one(myquery, newvalues)

        to_send_to_abs = {
            'id': id,
            'predicate': predicate
        }
        print("hererer")
        json_object = json.dumps(to_send_to_abs)
        url = 'http://0.0.0.0:9004/playground_signature'
        x = requests.post(url, data = json_object)
        generated_response = json.loads(x.text)
        if generated_response == 'error':
            return JsonResponse({"response": "error"}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:        
            return JsonResponse(generated_response, safe=False, status=status.HTTP_200_OK)
    return JsonResponse({"response": "error"}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def verify_signature(request):
    if request.method == 'POST':
        mongo_client = MongoClient()
        db = mongo_client.domain2
        col = db.api_hit_counter
        cursor = list(col.find({}))
        item =cursor[-1]
        id = item['id']
        id = int(id)
        
        time_to_generate_keys = request.POST.__getitem__("time")
        predicate = request.POST.__getitem__("predicate")
        attributes = request.POST.__getitem__("attributes")
        to_send_to_domain1 = {
            "api_number": id,
            "tpk": request.POST.__getitem__("tpk"),
            "apk": request.POST.__getitem__("apk"),
            "sign": request.POST.__getitem__("sign")
        }
        json_object = json.dumps(to_send_to_domain1)
        
        start_time_api = time.time()
        
        url = 'http://localhost:8000/pep/api/verify_signature'
        x = requests.post(url, data = json_object)
        
        end_time_api = time.time()
        
        y = json.loads(x.text)
        if y['response'] == 'True':
            time_diff = end_time_api - start_time_api
            overall_time = time_diff + float(time_to_generate_keys)
            csvRow = str(id) + "," + predicate + "," +str(attributes)+","+str(time_to_generate_keys)+","+str(overall_time)+","+y['response']
            # print(csvRow)
            with open('time_with_generated_keys.csv', 'a', newline='') as fd:
                fd.write(csvRow)
                fd.write("\n")
            
            return JsonResponse({"response":"True"}, status=status.HTTP_200_OK)
        else:
            time_diff = end_time_api - start_time_api
            overall_time = time_diff + float(time_to_generate_keys)
            csvRow = str(id) + "," + predicate + "," +str(attributes)+","+str(time_to_generate_keys)+","+str(overall_time)+","+y['response']
            # print(csvRow)
            with open('time_with_generated_keys.csv', 'a', newline='') as fd:
                fd.write(csvRow)
                fd.write("\n")
            return JsonResponse({"response":"False"}, status=status.HTTP_200_OK)


# Views for playground 2 (stored keys)
@csrf_exempt
def generate_keys_and_store(request):
    if request.method == 'POST':
        predicate = request.POST.__getitem__("predicate")
        # print(predicate)
        to_send_to_abs = {
            'predicate': predicate
        }
        json_object = json.dumps(to_send_to_abs)
        r = requests.post('http://0.0.0.0:9004/playground_signature2', data=json_object)
        y = json.loads(r.text)
        store_predicate = PredicateKeys()
        store_predicate.predicate = predicate
        store_predicate.tpk = y['tpk']
        store_predicate.predicate_length = y['attribute_length']
        store_predicate.apk = y['apk']
        store_predicate.ask = y['ask']
        store_predicate.sign = y['signature']
        store_predicate.save()
    return JsonResponse({"response":"True"}, status=status.HTTP_200_OK)

@csrf_exempt
def remove(request):
    if request.method == 'POST':
        print(request.POST.__getitem__("predicate"))
        predicate = request.POST.__getitem__("predicate")
        PredicateKeys.objects.filter(predicate=predicate).delete()
    return JsonResponse({"response":"True"}, status=status.HTTP_200_OK)

@csrf_exempt
def keys_to_find_time(request):
    if request.method == 'POST':
        print(request.POST.__getitem__("predicate"))
        predicate = request.POST.__getitem__("predicate")
        mongo_client = MongoClient()
        db = mongo_client.domain2
        col = db.api_hit_counter2
        start_time_api = time.time()
        cursor = list(col.find({}))
        item =cursor[-1]
        id = item['id']
        id = int(id)
        myquery = { "id": id }
        id = id + 1
        print(id)
        newvalues = { "$set": { "id": id }}
        col.update_one(myquery, newvalues)
        data = PredicateKeys.objects.get(predicate=predicate)
        to_send_to_domain1 = {
            "api_number": id,
            "tpk": data.tpk,
            "apk": data.apk,
            "sign": data.sign
        }
        json_object = json.dumps(to_send_to_domain1)
        
        url = 'http://localhost:8000/pep/api/verify_signature'
        x = requests.post(url, data = json_object)
        y = json.loads(x.text)
        end_time_api = time.time()
        if y['response'] == 'True':
            time_diff = end_time_api - start_time_api
            csvRow = str(id) + "," + predicate + "," +str(data.predicate_length)+","+str(time_diff)+","+y['response']
            with open('time_with_stored_keys.csv', 'a') as fd:
                fd.write(csvRow)
                fd.write("\n")
            return JsonResponse({"response":"True"}, status=status.HTTP_200_OK)
        else:
            time_diff = end_time_api - start_time_api
            csvRow = str(id) + "," + predicate + "," +str(data.predicate_length)+","+str(time_diff)+","+y['response']
            with open('time_with_stored_keys.csv', 'a') as fd:
                fd.write(csvRow)
                fd.write("\n")
            return JsonResponse({"response":"False"}, status=status.HTTP_200_OK)
