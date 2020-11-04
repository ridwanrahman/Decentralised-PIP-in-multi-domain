from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib import messages

from .models import Policy, CustomABACUser, Resource, ResourceDescription

# Create your views here.
def index(request):
    # return "hi"
    return render(request, "main/base.html", {})

def home(request):
    return render(request, "home.html", {"email":"radf"})

def login_page(request):
    return render(request, "login.html", {})

def login_process_form(request):
    username = request.POST['inputEmail']
    password = request.POST['inputPassword']
    user = authenticate(username=username, password=password)
    # print(user)
    # print(request.user.is_authenticated)
    if user is not None:
        print(user.is_superuser)
        login(request, user)
        if(user):
            return redirect('/adminPanel/dashboard')
    else:
        return render(request, "login.html", {})

def logout_view(request):
    logout(request)
    return render(request, "login.html", {})

@login_required
def dashboard(request):
    users =CustomABACUser.objects.all().count()
    print(users)
    resources = Resource.objects.all().count()
    policies = Policy.objects.all().count()
    return render(request, "logged_in_templates/dashboard.html", {"users":users,
                                                                    "resources":resources,
                                                                    "policies":policies})


# Users
def users_page(request):
    users = CustomABACUser.objects.filter(is_superuser=False)
    return render(request,"logged_in_templates/users/user.html", {"users":users})

def add_user(request):
    return render(request,"logged_in_templates/users/add_users.html", {})

def user_add_process(request):
    if request.method == 'POST':
        print(request.POST['email'])
        user = CustomABACUser()
        num_results = CustomABACUser.objects.filter(email = request.POST['email']).count()
        if(num_results == 0):
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.username = request.POST['email']
            user.set_password(request.POST['password'])
            user.designation = request.POST['designation']
            user.age = request.POST['age']
            user.role = request.POST['role']
            user.organization = request.POST['organization']
            user.suburb = request.POST['suburb']
            user.city = request.POST['city']
            user.state = request.POST['state']
            user.country = request.POST['country']
            user.save()
            messages.success(request, "User saved successfully",extra_tags='primary')
        else:
            messages.error(request, "User with same email address already exists",extra_tags='danger')
    return render(request,"logged_in_templates/users/add_users.html", {})

# Resources
def resources_page(request):
    resources = Resource.objects.all()
    return render(request,"logged_in_templates/resources/resources.html", {"resources":resources})

def add_resource_page(request):
    policies = Policy.objects.all()
    print(policies)
    return render(request, "logged_in_templates/resources/add_resource.html", {"policies":policies})

def edit_resource(request, id):
    if request.method=='POST':
        print("edit resource button clicked")
        print(request.POST)
        resource = Resource.objects.get(id=id)
        resource.resource_name = request.POST['resource_name']
        resource.viewable = request.POST['viewable']
        resource.policy  = Policy.objects.get(policy_name=request.POST['policy'])
        resource.save()
        try:
            resource_description = ResourceDescription.objects.get(resource=resource.id)
        except ResourceDescription.DoesNotExist:
            resource_description = ResourceDescription()
            resource_description.resource = Resource.objects.get(resource_name=request.POST['resource_name'])
            resource_description.creator=CustomABACUser.objects.get(id=request.user.id)
        # resource_description.resource = Resource.objects.get(resource=resource.id)
        # resource_description.creator = CustomABACUser.objects.get(email=request.user.email)
        resource_description.resource_description_1 = \
                                request.POST['resource_description_1']
        resource_description.resource_description_2 = \
                                request.POST['resource_description_2']
        resource_description.resource_description_3 = \
                                request.POST['resource_description_3']
        resource_description.resource_description_4 = \
                                request.POST['resource_description_4']
        resource_description.resource_description_5 = \
                                request.POST['resource_description_5']
        resource_description.save()
        messages.success(request, "Resource edited successfully",extra_tags='primary')
        policies = Policy.objects.all()
        resource = Resource.objects.get(id=id)
        resource_description = ResourceDescription.objects.get(resource=resource.id)
        return render(request, "logged_in_templates/resources/edit_resource.html", {"resource": resource,
                                                                                    "policies": policies,
                                                                                    "resource_description": resource_description})
    else:
        policies = Policy.objects.all()
        resource = Resource.objects.get(id=id)
        # print(resource.resource_name)
        try:
            resource_description = ResourceDescription.objects.get(resource=resource.id)
        except ResourceDescription.DoesNotExist:
            resource_description = None
        # print(resource_description.resource_description_1)
        return render(request, "logged_in_templates/resources/edit_resource.html", {"resource": resource,
                                                                                    "policies": policies,
                                                                                    "resource_description": resource_description})


def resource_add_process(request):
    if request.method == 'POST':
        resource = Resource()
        resource.resource_name = request.POST['resource_name']
        resource.viewable = request.POST['viewable']
        resource.policy  = Policy.objects.get(policy_name=request.POST['policy'])
        resource.save()
        resource_description = ResourceDescription()
        resource_description.resource = Resource.objects.get(resource_name=request.POST['resource_name'])
        resource_description.creator = CustomABACUser.objects.get(email=request.user.email)
        resource_description.resource_description_1 = \
                                request.POST['resource_description_1']
        resource_description.resource_description_2 = \
                                request.POST['resource_description_2']
        resource_description.resource_description_3 = \
                                request.POST['resource_description_3']
        resource_description.resource_description_4 = \
                                request.POST['resource_description_4']
        resource_description.resource_description_5 = \
                                request.POST['resource_description_5']
        resource_description.save()
        messages.success(request, "Resource saved successfully",extra_tags='primary')
    return render(request, "logged_in_templates/resources/add_resource.html", {})

# Policy
def policy_page(request):
    policies = Policy.objects.all()
    return render(request, "logged_in_templates/policies/policy.html", {"policies":policies})

def add_policy_page(request):
    return render(request, "logged_in_templates/policies/add_policy.html", {})

def policy_add_process(request):
    if request.method == 'POST':
        custom_user = CustomABACUser.objects.get(email=request.user.email)
        myDict = dict(request.POST)
        policy = Policy()
        policy_name = myDict['policy_name']
        policy.policy_name = policy_name[0].strip('[]')
        policy.user = custom_user
        policy_description = myDict['policy_description']
        policy.policy_description = policy_description[0].strip('[]')
        policy_version = myDict['policy_version']
        policy.policy_version = policy_version[0].strip('[]')
        subject_name = myDict['subject_name']
        policy.subject_name = str(subject_name).strip('[]').replace("'","")
        subject_value = myDict['subject_value']
        policy.subject_value = str(subject_value).strip('[]').replace("'","")
        action_name = myDict['action_name']
        policy.action_name = str(action_name).strip('[]').replace("'","")
        action_value = myDict['action_value']
        policy.action_value = str(action_value).strip('[]').replace("'","")
        # resource_name = myDict['resource_name']
        # policy.resource_name = str(resource_name).strip('[]').replace("'","")
        # resource_value = myDict['resource_value']
        # policy.resource_value = str(resource_value).strip('[]').replace("'","")
        environment_name = myDict['environment_name']
        policy.environment_name = str(environment_name).strip('[]').replace("'","")
        environment_value = myDict['environment_value']
        policy.environment_value = str(environment_value).strip('[]').replace("'","")
        policy.save()
    return render(request, "logged_in_templates/policies/add_policy.html", {})
