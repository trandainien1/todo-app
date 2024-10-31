from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import MyUserCreationForm, TaskForm

@login_required(login_url='login')
def home(request):
    form = TaskForm()
    tasks = request.user.task_set.all()
    completed_tasks = request.user.task_set.filter(completed=True)
    todo_tasks = request.user.task_set.filter(completed=False)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')

    context = {
        'tasks': tasks, 
        'form': form,
        'completed_tasks': completed_tasks,
        'todo_tasks': todo_tasks,
    }
    return render(request, 'base/home.html', context)

def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    
    return redirect('home')

def edit_task(request, pk):
    task = Task.objects.filter(id=pk)
    
    return 

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exit')

    context = {}
    return render(request, 'base/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def signup(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {'form': form}
    return render(request, 'base/signup.html', context)

def toggle_task(request, id):
    task = Task.objects.get(id=id)
    if task:
        task.completed = not task.completed
        task.save()
    return redirect('home')
    