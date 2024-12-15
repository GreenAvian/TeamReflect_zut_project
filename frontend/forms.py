from django import forms

from .models import Person

class NameForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email']  # Specify fields to include in the form