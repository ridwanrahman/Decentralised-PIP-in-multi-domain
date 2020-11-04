from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('adminPanel/', adminPanel.urls)
    
    # GET all Resource
    path('resources/', resource_list),

    path('resources/<slug:name>', specific_resource_description),
    
    #GET specific resource
    path('resources/<int:id>/', get_specific_resource),

    #Get all policies
    path('policies/', policy_list),

    #GET specific policy
    path('policies/<int:id>/policy', get_specific_policy),
    
    #GET access structure of specific policy
    path('policies/<int:id>/access_structure', get_policy_access_structure),
]