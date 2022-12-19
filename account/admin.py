from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['username','phone_number']
    list_filter = ['is_admin',]
    fieldsets = (
        (None, {'fields':('username','password')}),
        ('Personal Info',{'fields':('phone_number','is_send_sms')}),
        ('Permissions',{'fields':('is_admin','is_active')}),
    )

    add_fieldsets = (
        (None,{
            'classes':('wide'),
            'fields':('username','password1','password2')
        }),
    )

    filter_horizontal = ()

admin.site.register(Account, UserAdmin)