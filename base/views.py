from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
import datetime
from hospital.models import SickItem, Hospital, Doctor
from .forms import AddHospitalForm, AddDoctorForm
from .auth import DoctorAuthentication

def home(request):
    if request.user.is_authenticated:
        sick_items = SickItem.objects.filter(account=request.user)
    
    else:
        return redirect('login')

    context = {
        'sick_items':sick_items
    }

    return render(request, 'main/index.html', context)

def main_organization(request):
    if request.user.is_authenticated:
        hospitals = Hospital.objects.all().order_by('-created_date')
        doctors = Doctor.objects.all().order_by('-created_date')
    else:
        return redirect('login')

    context = {
        'hospitals':hospitals,
        'doctors':doctors
    }

    return render(request, 'main/organization_index.html', context)

def add_hospital(request):

    if request.method == "POST":
        form = AddHospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organizations')
    else:
        form = AddHospitalForm

    context = {
        'form':form
    }

    return render(request, 'details/add-hospital.html', context)

def add_doctor(request):

    if request.method == "POST":
        form = AddDoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organizations')
    else:
        form = AddDoctorForm

    context = {
        'form':form
    }

    return render(request, 'details/add-doctor.html', context)

def auth_doctor(request):

    if request.method == "POST":
        username = request.POST['username']
        user = DoctorAuthentication.authenticate(request, username=username)
        if user is not None:
            login(request, user)
            return redirect('index-doctor',slug=user.slug)
        else:
            return redirect('auth-doctor')

    return render(request, 'auth/auth-doctor.html')

def index_doctor(request, slug):

    doctor = Doctor.objects.get(slug=slug)
    sicks = doctor.sick_list.through.objects.filter(weekday=datetime.date.today()).order_by('-order')

    if request.method == "POST":
        date = request.POST['input-date']
        sicks = doctor.sick_list.through.objects.filter(doctor__slug=doctor.slug ,weekday=date)

    context = {
        'doctor':doctor,
        'sicks':sicks
    }

    return render(request, 'main/index_doctor.html', context)