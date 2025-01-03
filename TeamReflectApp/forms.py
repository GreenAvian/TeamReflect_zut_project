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

    created_by = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)
    
    priority = forms.ChoiceField(
        choices=[],
        widget=forms.Select(),
        label="Priority",
        required=True
    )

    class Meta:
        model = Feedback
        fields = ['title', 'priority', 'content', 'rating', 'created_by']  # Specify fields to include in the form

    def __init__(self, *args, **kwargs): 
            super().__init__(*args, **kwargs)
            self.fields['priority'].choices = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]