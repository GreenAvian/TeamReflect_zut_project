from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-form'}),
        label="1-5 rating",
        required=True 
    )
    
    class Meta:
        model = Feedback
        fields = ['type', 'priority', 'created_by', 'content', 'status', 'rating']  # Specify fields to include in the form
