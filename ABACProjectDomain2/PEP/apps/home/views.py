from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .models import CustomABACUser
from apps.api.models import *

# Create your views here.
def home(request):
    return render(request, "home.html", {})

def login_page(request):
    return render(request, "login.html", {})

def process_login(request):
    if request.method == 'POST':
        email = request.POST['inputEmail']
        password = request.POST['inputPassword']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            return render(request, "login.html", {})

def logout_function(request):
    print("logout view reached")
    logout(request)
    return redirect('/login')

@login_required
def dashboard(request):
    return render(request, "logged_in_templates/dashboard.html", {})

@login_required
def domain_resource(request):
    print("herere")
    return render(request, "logged_in_templates/domain_resource/resource.html", {})

def signup(request):
    return render(request, "signup.html", {})

def signup_process(request):
    if request.method =='POST':
        username = request.POST['email_address']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email_address = request.POST['email_address']
        password = request.POST['password']
        designation = request.POST['designation']
        role = request.POST['role']
        age = request.POST['age']
        organization = request.POST['organization']
        suburb = request.POST['suburb']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']

        user = CustomABACUser()
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email_address
        user.set_password(password)
        user.designation = designation
        user.role = role
        user.age = age
        user.organization = organization
        user.suburb = suburb
        user.city = city
        user.state = state
        user.country = country
        user.save()
        return redirect('/login')


# playground
@login_required
def playground_page(request):
    return render(request, "logged_in_templates/playground.html", {})

#playground 2
def playground2_page(request):
    data = PredicateKeys.objects.all()
    return render(request, "logged_in_templates/playground2.html", {'data':data})

