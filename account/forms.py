from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from .models import Account

class RegisterUserForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'name':"password1", 'id':"password1", 'type':"password", 'class':"form-control", 'placeholder':"Parol"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'name':"password2", 'id':"password2", 'type':"password", 'class':"form-control", 'placeholder':"Parolni takrorlang"}))

    class Meta:
        model = Account
        fields = ('username','phone_number')

        labels = {
            'username':'',
            'phone_number':''
        }

        widgets = {
            'username':forms.TextInput(attrs={'name':"name", 'id':"name", 'type':"text", 'class':"form-control", 'placeholder':"To'liq ism" }),
            'phone_number':forms.NumberInput(attrs={'name':"phone", 'id':"phone", 'type':"text", 'class':"form-control", 'placeholder':"Telefon raqam"})
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField

    class Meta:
        model = Account
        fields = ('username','phone_number')