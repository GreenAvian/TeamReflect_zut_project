from django import forms

from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['type', 'priority', 'created_by', 'content', 'status']  # Specify fields to include in the form