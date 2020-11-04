from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/resources', get_all_resources),
    path('api/resources/<slug:name>', get_resource_description),
    path('api/policies', get_policies),
    path('api/policies/<int:id>/policy', get_specific_policy),
    path('api/policies/<int:id>/access_structure', get_policy_access_structure),
]