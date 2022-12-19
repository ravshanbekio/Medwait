from django.contrib import admin
from .models import City, Hospital, Department, Doctor, SickItem, SicknessList

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','department','created_date']
    list_filter = ['department__name','first_name','last_name']


    fieldsets = (
        ("Personal info", {'fields':('first_name','last_name')}),
        ("About",{'fields':('hospital','department','description','preview_photo','work_start_time','work_end_time')}),
        #("Sicks", {'fields':('sick_list',)}),
        ("Advanced data", {'fields':('slug','username')})
    )

admin.site.register(City)
admin.site.register(Hospital)
admin.site.register(Department)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(SickItem)
admin.site.register(SicknessList)