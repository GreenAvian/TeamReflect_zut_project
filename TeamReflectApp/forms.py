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
        widget=forms.RadioSelect(attrs={'class': 'feedback-rating-form'}),
        label="1-5 rating",
        required=True 
    )

    created_by = forms.CharField(
        widget=forms.HiddenInput(),
        required=False)
    
    priority = forms.ChoiceField(
        choices=[('Wysoki', 'Wysoki'), ('Średni', 'Średni'), ('Niski', 'Niski')],
        widget=forms.Select(attrs={'class': 'feedback-priority-form'}),
        label="Priority",
        required=True
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'feedback-title-form', 'placeholder': 'Tytuł'}),
        label="Title",
        required=True
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'feedback-content-form', 'placeholder': 'Feedback'}),
        label="Content",
        required=True
    )

    class Meta:
        model = Feedback
        fields = ['title', 'content', 'rating', 'priority', 'created_by']  # Specify fields to include in the form
