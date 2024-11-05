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
    # tasks = request.user.task_set.all()
    nav_text_colors = ['gray'] * 3
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')

    if filter_type == 'todo':
        page_title = 'To Do Tasks'
        tasks = request.user.task_set.filter(completed=False) 
        nav_text_colors[2] = 'blue'
        current_page = 'todo'
    elif filter_type == 'completed':
        page_title = 'Completed Tasks'
        # tasks = Task.objects.filter(completed=True) 
        tasks = request.user.task_set.filter(completed=True) 
        nav_text_colors[1] = 'blue'
        current_page = 'completed'
    else:
        page_title = 'All Tasks'
        # tasks = Task.objects.all()
        tasks = request.user.task_set.all() 
        nav_text_colors[0] = 'blue'
        current_page = 'all'

    tasks = tasks.order_by('-id')

    context = {
        'tasks': tasks, 
        'form': form,
        'page_title': page_title,
        'nav_text_colors': nav_text_colors,
        'current_page': current_page
    }
    return render(request, 'base/home.html', context)

def delete_task(request, pk):
    page_title = request.GET.get('page')
    task = Task.objects.get(id=pk)

    task.delete()
    tasks = Task.objects.all() 
    context = {
        'tasks': tasks
    }

    if page_title == 'All Tasks':
        return redirect('home')
    elif page_title == 'To Do Tasks':
        return redirect('/filter-task/todo')
    else:
        return redirect('/filter-task/completed')

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
    
    if page_title == 'all':
        return redirect('home')
    elif page_title == 'todo':
        return redirect('home', 'todo')
    else:
        return redirect('home', 'completed')

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

def add_task(request, pk=None):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        due_time = request.POST.get('due_time')
        
        if title != '' and description != '' and due_date != '' and due_time != '':
            if pk == None:
                new_task = Task(
                    title=title,
                    description=description,
                    due_date=due_date,
                    due_time=due_time,
                    completed=False,
                    user=request.user,
                )
                new_task.save()
            else:
                task = Task.objects.get(id=pk)
                
                task.title=title
                task.description=description
                task.due_date=due_date
                task.due_time=due_time
                
                task.save()

            return redirect('home')
        else:
            messages.error(request, 'Please fill out all the fields')

    if pk == None: # if user press 'add task'
        return render(request, 'base/add_task.html', {'task': None})
    else:
        task = Task.objects.get(id=pk)
        print(task)
        task_form = TaskForm(instance=task)
        
        return render(request, 'base/add_task.html', {'task': task, 'form': task_form})