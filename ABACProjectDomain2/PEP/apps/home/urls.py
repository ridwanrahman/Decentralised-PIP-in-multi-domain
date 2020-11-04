from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home),
    path('login', login_page),
    path('login_submit', process_login),

    path('signup', signup),
    path('signup_process', signup_process),


    path('dashboard', dashboard),
    path('domain_resource', domain_resource),

    path('playground', playground_page),
    path('playground2', playground2_page),

    path('logout', logout_function),
]