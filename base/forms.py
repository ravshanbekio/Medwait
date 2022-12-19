from django import forms
from hospital.models import Hospital, Doctor

class AddHospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ('city','name','description','address')

        labels = {
            'city':'',
            'name':'',
            'description':"Kasalxona haqida ma'lumot",
            'address':''
        }

        widgets = {
            'city': forms.Select(attrs={'class':'form-control','type':'select','name':'select-city','placeholder':'Shaharni tanlang'}),
            'name': forms.TextInput(attrs={'class':'form-control','type':'text','name':'input-name','placeholder':'Kasalxona nomi'}),
            'description': forms.Textarea(attrs={'class':'form-control','type':'textarea','name':'input-description','placeholder':"Qisqacha ma'lumot"}),
            'address':forms.TextInput(attrs={'class':'form-control','type':'text','name':'input-address', 'placeholder':'Kasalxona joylashgan manzil'})
        }

class AddDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('username','hospital','department','first_name','last_name','description','preview_photo','work_start_time','work_end_time')

        labels = {
            'hospital':'Kasalxona',
            'department':"Doktor yo'nalishi",
            'first_name':'',
            'last_name':'',
            'username':'',
            'description':"Doktor haqida ma'lumot",
            'preview_photo':'',
            'work_start_time':'',
            'work_end_time':'',
        }

        widgets = {
            'hospital': forms.Select(attrs={'class':'form-control','type':'select','name':'select-hospital'}),
            'department':forms.Select(attrs={'class':'form-control','type':'select','name':'select-department'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Ism'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Familiya'}),
            'username':forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Takrorlanmaydigan nom'}),
            'description':forms.Textarea(attrs={'class':'form-control','type':'textarea'}),
            'preview_photo':forms.FileInput(attrs={'class':'form-control','type':'file'}),
            'work_start_time':forms.DateTimeInput(attrs={'class':'form-control','placeholder':'Ish boshlanish vaqti'}),
            'work_end_time': forms.DateTimeInput(attrs={'class':'form-control','placeholder':'Ish yakunlash vaqti'})
        }