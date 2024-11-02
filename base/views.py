from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import MyUserCreationForm, TaskForm

@login_required(login_url='login')
def home(request, filter_type='all'):
    form = TaskForm()
    tasks = request.user.task_set.all()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')

    if filter_type == 'todo':
        page_title = 'To Do Tasks'
        tasks = Task.objects.filter(completed=False) 
    elif filter_type == 'completed':
        page_title = 'Completed Tasks'
        tasks = Task.objects.filter(completed=True) 
    else:
        page_title = 'All Tasks'
        tasks = Task.objects.all()

    context = {
        'tasks': tasks, 
        'form': form,
        'page_title': page_title,
    }
    return render(request, 'base/home.html', context)

def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    tasks = Task.objects.all() 
    context = {
        'tasks': tasks
    }
    
    return render(request, 'base/home.html', context)

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
    page_title = request.GET.get('page')
    task = Task.objects.get(id=id)
    if task:
        task.completed = not task.completed
        task.save()
        messages.error(request, 'Please fill all the fields')
    context = {}
    # return render(request, 'base/add_task.html', context)
    if page_title == 'All Tasks':
        return redirect('home')
    elif page_title == 'To Do Tasks':
        return redirect('/filter-task/todo')
    else:
        return redirect('/filter-task/completed')

def all_task(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
        'page_title': 'All tasks',
    }
    return render(request, 'base/home.html', context)

def completed_task(request):
    tasks = Task.objects.filter(completed=True)
    context = {
        'tasks': tasks,
        'page_title': 'Completed tasks',
    }
    return render(request, 'base/home.html', context)

def todo_task(request):
    tasks = Task.objects.filter(completed=False)
    context = {
        'tasks': tasks,
        'page_title': 'To do tasks',
    }
    return render(request, 'base/home.html', context)

def add_task(request):
    pass