from django import forms
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        
class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        
class DeleteReviewForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
# class FollowUsersForm(forms.Form):
#     class Meta:
#         model = User
#         fields = ['follows']
#     followed_user = forms.CharField(label=False, widget=forms.TextInput())