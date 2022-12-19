from django.urls import path
from .views import (selectDepartment, filterDoctors, getDoctor, 
                    addSick, deleteSick, allSickness, sicknessDetail)

urlpatterns = [
    path('department/',selectDepartment, name='departments'),
    path('doctors/<str:department>/',filterDoctors, name='filtered-doctors'),
    path('doctor/<slug:slug>/',getDoctor, name='get-doctor'),
    path('add-sick/<slug:slug>/',addSick, name='add-sick'),
    path('delete-sick/<slug:slug>/',deleteSick, name='delete-sick'),


    path('sickness/',allSickness, name='sickness-list'),
    path('sickness/<slug:slug>/',sicknessDetail, name='sickness-detail'),
]