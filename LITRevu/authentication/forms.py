from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from authentication.models import User

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'


class FollowUsersForm(forms.Form):
    followed_user = forms.CharField(max_length=100)
    # class Meta:
    #     model = User
    #     follows = forms.CharField(max_length=100)
    #     fields = ['follows']
        
    def __init__(self, *args, **kwargs):
        super(FollowUsersForm, self).__init__(*args, **kwargs)
        self.fields['followed_user'].widget.attrs['placeholder'] = "Nom d'utilisateur"