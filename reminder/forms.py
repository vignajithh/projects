from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from reminder.models import Todos



class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class LoginForm(forms.Form):
        username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control border border-light-subtle"}))
        password=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control border border-light-subtle"}))

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todos
        fields=["name"]


     
