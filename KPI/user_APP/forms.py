from django.contrib.auth.forms import UserCreationForm
from KPI_APP.models import User
from django import forms


class SignUp(UserCreationForm):
    class Meta:
        model = User
        fields = 'username', 'password1', 'password2'


class SignIn(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
