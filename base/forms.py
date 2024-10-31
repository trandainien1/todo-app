from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task, CustomUser

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['user', 'state', 'completed']
    
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

