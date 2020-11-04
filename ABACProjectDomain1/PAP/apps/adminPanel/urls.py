from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('adminPanel/', adminPanel.urls)
    path('index', index),
    path('home', home),
    path('login', login_page),
    path('login_submit', login_process_form),
    path('logout', logout_view),
    path('dashboard', dashboard),

    path('user', users_page),
    path('add_user', add_user),
    path('user_add_process', user_add_process),
    path('edit_resource/<int:id>', edit_resource),


    path('resources', resources_page),
    path('add_resource', add_resource_page),
    path('resource_add_process', resource_add_process),
    
    path('policy', policy_page),
    path('add_policy', add_policy_page),
    path('policy_add_process', policy_add_process),

]