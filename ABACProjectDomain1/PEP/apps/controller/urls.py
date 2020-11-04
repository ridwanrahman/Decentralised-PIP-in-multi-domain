from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('adminPanel/', adminPanel.urls)
    # path('index', index),
    path('', home),
    path('playground', playground),
    # path('login', login_page),
    # path('login_submit', login_process_form),
    # path('logout', logout_view),
    # path('dashboard', dashboard),

]