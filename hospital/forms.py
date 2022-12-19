from django import forms
from .models import SickAge

class SickAgeForm(forms.ModelForm):
    class Meta:
        model = SickAge
        fields = ('age',)

        labels = {
            'age':'',
        }

        widgets = {
            'age': forms.DateInput(attrs={'class':'form-control','placeholder':'Kasalning tug\'ilgan sanasi','type':'date'}),
        }