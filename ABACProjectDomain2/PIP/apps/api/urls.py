from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('PIP/api', include('apps.api.urls')),
    # path('admin/', admin.site.urls),
    path('get_user_attributes', get_user_attributes),
]