from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from authentication.models import User

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

class FollowUsersForm(forms.Form):
    followed_user = forms.CharField(max_length=100)
    # class Meta:
    #     model = User
    #     follows = forms.CharField(max_length=100)
    #     fields = ['follows']