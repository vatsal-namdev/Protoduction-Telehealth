from django.shortcuts import render, redirect
from .models import post, comment, query
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exist')
                return redirect('register')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Exist')
                return redirect('register')  

            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save();
                return redirect('login')   

        else:
            messages.info(request, 'Password not Same')
            return redirect('register')  

    else:             
        return render(request,'register.html')    


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials are Invalid')
            return redirect('login')  

    else:          
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def blog(request):
    bpost = post.objects.all()
    return render(request, 'blog.html',{'bpost':bpost})