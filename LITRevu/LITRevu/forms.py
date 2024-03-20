from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput, Textarea
from django_starfield import Stars
from django.forms.widgets import ClearableFileInput
from . import models

User = get_user_model()


class TicketForm(forms.ModelForm):
    # edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    image = forms.ImageField(
        label_suffix="", required=False, widget=ClearableFileInput, label=""
    )
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': TextInput(attrs={
                'class': 'ticket-input',
                'style': 'width: 970px;',
                'label': 'text',
                'id': 'ticket-title'
                }),
            'description': Textarea(attrs={
                'class': "ticket-input",
                'style': 'width: 970px;',
                'label': 'text',
                'id': 'ticket-description'
            })
        }
        
class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
class ReviewForm(forms.ModelForm):
    # edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    rating = forms.IntegerField(widget=Stars)
    class Meta:
        model = models.Review
        # rating = forms.IntegerField(widget=Stars)
        fields = ['headline', 'rating', 'body']
        widgets = {
            'headline': TextInput(attrs={
                'class': 'ticket-input',
                'style': 'width: 970px;',
                'id': 'review-headline'
                }),
            'body': Textarea(attrs={
                'class': "ticket-input",
                'style': 'width: 970px;',
                'id': 'review-body'
            })
        }
        labels = {
            'headline': 'text',
            'body': 'text'
        }
        
class DeleteReviewForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
class FollowUsersForm(forms.Form):
    followed_user = forms.CharField(widget=forms.Textarea, max_length=255, required=True)
    class Meta:
        model = User
        fields = ['follows', 'followed_user']
        
    def __init__(self, *args, **kwargs):
        super(FollowUsersForm, self).__init__(*args, **kwargs)
        self.fields['followed_user'].widget.attrs['placeholder'] = "Nom d'utilisateur"