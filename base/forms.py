from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task, CustomUser

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['user', 'state', 'completed']
        widgets = {
            'due_date': DateInput(),
            'due_time': TimeInput()
        }
    
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

