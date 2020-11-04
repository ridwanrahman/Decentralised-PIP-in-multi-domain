from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import CustomABACUser
from django.http.response import JsonResponse
import json
import ast
from rest_framework import status
from pymongo import MongoClient
# Create your views here.

@csrf_exempt
def get_user_attributes(request):
    print("PIP CALLED")
    if request.method == 'POST':
        print("it was a post req")
        # print(request.POST)
        user = request.POST.__getitem__("user")
        print(user)
        attributes = request.POST.__getitem__("attributes")
        # print(attributes)
        res = json.loads(attributes)
        print(res)
        # print(res['subject_name'])
        # print(res['environment_name'])
        subject = res['subject_name']
        environment = res['environment_name']
        # print("check vals")
        print(subject == None)
        print(environment == None)
        if subject ==None:
            subject = ''
        if environment == None:
            environment = ''
        # print(len(subject))
        # print(len(environment))
        combined = ""
        li = []
        
        if len(subject) > 0 and len(environment)== 0:
            print("subject workd")
            subject = res['subject_name'].replace(" ", "")
            combined = combined + subject
        
        if len(environment) > 0 and len(subject) == 0:
            print("environment workd")
            environment = res['environment_name'].replace(" ", "")
            combined = combined + environment
        
        if len(environment) > 0 and len(subject) > 0:
            subject = res['subject_name'].replace(" ", "")
            environment = res['environment_name'].replace(" ", "")
            combined = subject +","+ environment

        print("combined: ", combined)
        li = list(combined.split(","))
        print(li)

        mongo_client = MongoClient()
        db = mongo_client.domain2
        col = db.home_customabacuser
        
        attribute_names=[]
        attribute_values=[]
        myquery = {
            "email":user
        }
        docs = col.find(myquery)
        for doc in docs:
            for key, value in doc.items():
                attribute_names.append(key)
        list_contains_checker = (all(elem in attribute_names for elem in li))
        print(list_contains_checker)
        if list_contains_checker == False:
            return JsonResponse({"response":"missing attributes"}, safe=False, status=status.HTTP_404_NOT_FOUND)
        else:
            docs = col.find(myquery)
            for doc in docs:
                for key, value in doc.items():
                    if key in li:
                        attribute_values.append(value)
                        # print("key: {0}, value: {1}".format(key, value))
            print(attribute_values)
            combined_attribute_values = ""
            for i in attribute_values:
                combined_attribute_values = combined_attribute_values +i+','
            
            # if res['action_name'] != None:
            #     action = res['action_name'].replace(" ", "")
            #     combined_attribute_values = combined_attribute_values +action+','
            if res['resource_name'] != None:
                resource = res['resource_name'].replace(" ", "")
                combined_attribute_values = combined_attribute_values +resource+','
            combined_attribute_values = combined_attribute_values[:-1]
            
            to_send = {
                'attributes':combined_attribute_values
            }
            print(to_send)
            return JsonResponse(to_send, safe=False, status=status.HTTP_200_OK)