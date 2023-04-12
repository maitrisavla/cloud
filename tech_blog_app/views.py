from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Blog, Category
from .forms import ContactForm, FeedbackForm
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.db import IntegrityError


def index(request):
    blog = Blog.objects.all().order_by('-date_upload')
    categories = Category.objects.all()
    return render(request, 'index.html', {'blog' : blog, 'categories':categories})

def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user)
                return redirect('index')
            else:
                error_message = "Invalid login credentials. Please try again."
                return render(request, 'login.html', {'error_message': error_message})
        return render(request,'login.html')
    return redirect('index')

def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            # Add validation for input fields here
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user = authenticate(username=username, password=password)
                django_login(request, user)
                return redirect('home')
            except IntegrityError:
                error_message = "Username or email already exists."
                return render(request, 'registration.html', {'error_message': error_message})
        else:
            return render(request, 'registration.html')
    return redirect('index')

def logout(request):
    if request.user.is_authenticated:
        django_logout(request)
        return redirect('login')
    return redirect('index')

def categories(request, name):
    listcat = Category.objects.all()
    categories = Category.objects.filter(name=name)
    blog = Blog.objects.filter(category = name).order_by('-date_upload')
    context = {'categories':categories, 'blog': blog, 'listcat': listcat}
    return render(request, 'categories.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message is received We will contact you shortly.')
            return redirect('contact')
    return render(request, 'contact.html')

def blog(request,slug):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'We love to hear from our adoring fans. Thank you for your feedback.')
            return redirect('blog', slug=slug)
    blog = Blog.objects.filter(slug=slug)
    categories = Category.objects.all()
    context = {'blog' : blog, 'categories':categories}
    return render(request, 'opened-blog.html', context)
