from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomABACUser)
admin.site.register(Policy)
admin.site.register(Resource)
admin.site.register(ResourceDescription)