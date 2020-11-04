from django.shortcuts import render
# from djongo import models
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from django.http.response import JsonResponse

# Create your views here.
def home(request):
    return render(request, "home.html", {})

@csrf_exempt
def playground(request):
    # e = PolicyAttributes()
    # e.attributes = {
    #     "name": "Djongo"
    # }
    # e.save()
    mongo_client = MongoClient()
    db = mongo_client.domain1
    col = db.controller_policyattributes
    cursor = list(col.find({}))
    item =cursor[-1]
    print(item)
    # print(type(item['attributes']))
    print(item['attributes'])
    attributes = item['attributes'].replace("'","").replace("{","").replace("}","")
    print(attributes)
    if request.method == 'POST':
        print("hererere")
        attributes = request.POST.__getitem__("attributes")
        print(attributes)
        e = PolicyAttributes()
        e.attributes = {
            attributes
        }
        e.save()
        return JsonResponse({"response":"True"})
    return render(request, "logged_in_templates/playground.html", {'attributes':attributes})