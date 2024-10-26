from django.contrib import admin

# Register your models here.
from .models import Task, CustomUser

admin.site.register(Task)
admin.site.register(CustomUser)
