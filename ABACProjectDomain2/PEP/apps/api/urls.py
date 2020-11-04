from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('', home),
    path('get_access_structure', get_access_structure),
    path('generate_signature', generate_signature),

    path('playground_generate_signature', playground_generate_signature),
    path('verify_signature', verify_signature),

    path('generate_keys_and_store', generate_keys_and_store),
    path('keys_to_find_time', keys_to_find_time),
    path('remove', remove),
]