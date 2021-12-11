from django import forms
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm, SignUpForm
from django.contrib import  messages
from .models import Post
from .forms import Postform
from django.contrib.auth.models import Group

# Home
def home(request):
    posts= Post.objects.all() 
    return render(request, 'Blog/home.html', {'posts':posts})
# About
def about(request):
    return render(request, 'Blog/about.html')
# Contact
def contact(request):
    return render(request, 'Blog/contact.html')


# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts= Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all() 
        return render(request, 'Blog/dashboard.html',{'posts':posts,'full_name':full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request = request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request, 'You have Successfully Login!!')
                    return HttpResponseRedirect('/dashboard/')
        else:            
            form = LoginForm
        return render(request, 'Blog/login.html', {'form':form})
    else:
      return HttpResponseRedirect('/dashboard/')  

# Singin
def signup(request):
    if request.method == 'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Congratulations!! you become an Author')
            user = fm.save()
            group = Group.objects.get(name='Author') 
            user.groups.add(group)
    else:        
        fm = SignUpForm()
    return render(request, 'Blog/signup.html', {'form':fm}) 



# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# ADD post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Postform(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                disc = form.cleaned_data['disc']
                pst = Post(title=title, disc=disc)
                pst.save()
                form = Postform()
        else:        
            form = Postform()
        return render(request, 'Blog/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')  


#Update post 
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = Postform(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = Postform(instance=pi)
        return render(request, 'Blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')  


#Update post 
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return render(request, 'Blog/dashboard.html')
    else:
        return HttpResponseRedirect('/login/')  