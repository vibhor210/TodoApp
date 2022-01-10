from django.contrib.auth import authenticate , logout , login as loginUser
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from todoapp.models import TODO
from todoapp.forms import TODOForm

# Create your views here.
@login_required(login_url='login')
def index(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user = user)
        return render(request,"index.html",context={'form' : form, 'todos' : todos})
    
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        context = {
            "form" : form
        }
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request , user)
                return redirect('home')
        else:
            return render(request,"login.html",context=context)

    else:
        form = AuthenticationForm()
        context = {
            "form" : form
        }
        return render(request,"login.html",context=context)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        context = {
            "form" : form
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('login')
        else:
            return render(request,"signup.html",context=context)
    else:
        form = UserCreationForm()
        context = {
            "form" : form
        }
        return render(request,"signup.html", context=context)

def signout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return redirect('home')
        else:
            return render(request,'index.html',context={'form':form})

def delete_todo(request,id):
    TODO.objects.get(pk = id).delete()
    return redirect('home')

def change_todo(request,id,status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect('home')