from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages, auth

# Create your views here.


def home(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            password = user_form.cleaned_data['password']
            user = user_form.save(commit=False)
            user.set_password(password)
            user.save()
            messages.success(
                request, "User registered. You can now Login !!!")
            
            return redirect('home')
        
    else:
        user_form = UserForm()

    context = {
        'form': user_form
    }
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    messages.success(request, "You are now logged out")
    return redirect('home')