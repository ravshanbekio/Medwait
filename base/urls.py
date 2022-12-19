from django.urls import path
from .views import home, main_organization ,add_hospital, add_doctor, auth_doctor, index_doctor

urlpatterns = [
    path('',home, name='home'),
    path('organizations/',main_organization, name='organizations'),
    path('myaccount/<slug:slug>/',index_doctor, name='index-doctor'),
    path('add-hospital/',add_hospital, name='add-hospital'),
    path('add-doctor/',add_doctor, name='add-doctor'),
    path('auth-doctor/',auth_doctor,name='auth-doctor'),
]