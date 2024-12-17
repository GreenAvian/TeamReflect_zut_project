from django import forms

from .models import Person, Feedback

class NameForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email']  # Specify fields to include in the form

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['type', 'priority', 'created_by', 'content', 'status']  # Specify fields to include in the form