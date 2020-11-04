from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('adminPanel/', adminPanel.urls)
    path('', home),
    # path('home', home),
    # path('login', login_page),
    # path('dashboard', dashboard),
]