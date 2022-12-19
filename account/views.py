from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .auth import AccountAuthentication
from .forms import RegisterUserForm

def signup(request):
    form = RegisterUserForm
    if request.method == "POST":
        form = RegisterUserForm(request.POST or None)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password1']
            form.save()
            user = AccountAuthentication.authenticate(request, phone_number=phone_number, password=password)
            login(request, user)
            return redirect('home')

    context = {
        'form':form
    }

    return render(request, 'signup.html', context)

def signin(request):
    if request.method == "POST":
        phone_number = request.POST['phone']
        password = request.POST['password']
        user = AccountAuthentication.authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('login')