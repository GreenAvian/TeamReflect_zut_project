from django import forms
from django.contrib.auth.models import User, Group
from .models import Feedback, LeaderPost

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
        widget=forms.TextInput(attrs={'class': 'feedback-title-form', 'placeholder': 'Temat'}),
        label="Title",
        required=True
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'feedback-content-form', 'placeholder': 'Feedback'}),
        label="Content",
        required=True
    )


        # Fields for foreign key relationships
    for_post = forms.ModelChoiceField(
        queryset=LeaderPost.objects.all(),
        widget=forms.Select(attrs={'class': 'feedback-for-post-form'}),
        label="For Post",
        required=False
    )
    
    for_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'feedback-for-user-form'}),
        label="For User",
        required=False
    )
    
    for_group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'feedback-for-group-form'}),
        label="For Group",
        required=False
    )


    class Meta:
        model = Feedback
        fields = ['title', 'content', 'rating', 'priority', 'created_by', 'for_post', 'for_user', 'for_group']  # Specify fields to include in the form
