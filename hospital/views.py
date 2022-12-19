from django.shortcuts import render, redirect
from .models import Department, Doctor, City, SicknessList
from .forms import SickAgeForm
from .utils import searchSickness
import datetime
from django.http import HttpResponse
import vonage

def selectDepartment(request):

    departments = Department.objects.all()

    context = {
        'departments':departments
    }

    return render(request, 'hospital/department.html', context)

def filterDoctors(request, department):

    doctors = Doctor.objects.filter(department__name=department)

    cities = City.objects.all()

    context = {
        'doctors':doctors,
        'cities':cities
    }

    return render(request, 'hospital/doctor.html', context)

def getDoctor(request, slug):

    doctor = Doctor.objects.get(slug=slug)

    sick_item = doctor.sick_list.through.objects.filter(doctor__slug=slug,
        weekday=datetime.date.today()).order_by('-order')

    context = {
        'doctor':doctor,
        'sick_item':sick_item
    }

    return render(request, 'hospital/doctor-single.html', context)

def addSick(request, slug):
    if request.user.is_authenticated:
        doctor = Doctor.objects.get(slug=slug)

        doctor.sick_list.add(request.user)
        doctor_item = doctor.sick_list.through.objects.get(account=request.user, doctor_id=doctor.id)
        doctor_item.weekday = request.POST['input-date']
        doctor_item.save()
        
        doctor_item = doctor.sick_list.through.objects.filter(doctor__slug=slug,
            weekday=datetime.date.today()).order_by('-order')
        get_client_for_send_sms = doctor_item[:3]
        for i in get_client_for_send_sms:
            if i.account.is_send_sms:
                return redirect('get-doctor',slug=slug)
            else:
                client = vonage.Client(key="65847809", secret="L8GwAnN0h4zHvgQZ")
                sms = vonage.Sms(client)

                responseData = sms.send_message(
                {
                    "from": "MedWait",
                    "to": f'{i.account.phone_number}',
                    "text": f"Hurmatli {i.account.username}, sizni {i.doctor.first_name} {i.doctor.last_name} doktori qabuliga navbatingiz kelganidan xabardor qilmoqchimiz. \nIltimos doktor qabulidan chiqqandan keyin ushbu havolaga kirib navbatingizni o'chirib yuboring: http://127.0.0.1:8000/delete-sick/{doctor.slug}",
                }
            )

            if responseData["messages"][0]["status"] == "0":
                print(f"{i.account.phone_number} profiliga SMS xabar yuborildi!")
            else:
                print(f"SMSni yuborishda xatolik: {responseData['messages'][0]['error-text']}")

            i.account.is_send_sms = True
            i.account.save()
                
    else:
        return redirect('login')

    return redirect('get-doctor',slug=slug)

def deleteSick(request, slug):
    if request.user.is_authenticated:
        doctor = Doctor.objects.get(slug=slug)

        doctor.sick_list.remove(request.user)
        request.user.is_send_sms = False
        request.user.save()
    
        doctor_item = doctor.sick_list.through.objects.filter(doctor__slug=slug,
            weekday=datetime.date.today()).order_by('-order')
        get_client_for_send_sms = doctor_item[:3]
        for i in get_client_for_send_sms:
            if i.account.is_send_sms:
                return redirect('detail',slug=slug)
            else:
                client = vonage.Client(key="79ec1c87", secret="H7cORMF1Dwytr8Cs")
                sms = vonage.Sms(client)

                responseData = sms.send_message(
                {
                    "from": "MedWait",
                    "to": f'{i.account.phone_number}',
                    "text": f"Hurmatli {i.account.username}, sizni {i.doctor.first_name} {i.doctor.last_name} doktori qabuliga navbatingiz kelganidan xabardor qilmoqchimiz. \nIltimos doktor qabulidan chiqqandan keyin ushbu havolaga kirib navbatingizni o'chirib yuboring: http://127.0.0.1:8000/delete-sick/{doctor.slug}",
                }
            )

            if responseData["messages"][0]["status"] == "0":
                print(f"{i.account.phone_number} profiliga SMS xabar yuborildi!")
            else:
                print(f"SMSni yuborishda xatolik: {responseData['messages'][0]['error-text']}")

            i.account.is_send_sms = True
            i.account.save()
        
    else:
        return redirect('login') 

    return redirect('get-doctor',slug=slug)

def allSickness(request):

    search_query, get_sickness = searchSickness(request)

    context = {
        'search_query':search_query,
        'get_sickness':get_sickness
    }

    return render(request, 'hospital/sickness.html', context)

def sicknessDetail(request, slug):

    sickness = SicknessList.objects.get(slug=slug)

    form = SickAgeForm
    medicine = sickness

    if request.method == "POST":
        form = SickAgeForm(request.POST or None)
        if form.is_valid():
            age = form.save(commit=False)
            if (datetime.date.today() - age.age) > datetime.timedelta(days=18*365):
                medicine = sickness.over_18
            elif (datetime.date.today() - age.age) > datetime.timedelta(days=120*365):
                return HttpResponse("Yosh juda katta. Iltimos, qayta kiriting")
            else:
                medicine = sickness.under_18
        
    context = {
        'form':form,
        'sickness':sickness,
        'medicine':medicine
    }   

    return render(request, 'hospital/sicknessdetail.html', context)