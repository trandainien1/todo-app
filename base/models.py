from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(null=True, unique=True)
    # name = models.CharField(max_length=200, null=True) 
    avatar = models.ImageField(null=True, default='')

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    REQUIRED_FIELDS = []
    

class Task(models.Model):
    title = models.CharField(max_length=30, blank=False,default='Empty')
    description = models.CharField(max_length=200, blank=False)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True)
    due_time = models.TimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.description[:50]


