# from typing_extensions import Required
from django import forms
from .models import Game 
from django.contrib.auth.models import User

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name','users']
        widgets = {'users':forms.CheckboxSelectMultiple}
    


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)



class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

