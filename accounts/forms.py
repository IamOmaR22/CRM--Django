from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User   # django default user model

class OrderForm(ModelForm): # name of the model and Form. and inherit from ModelForm.
    class Meta:
        model = Order # which model
        fields = '__all__' # which fields i will allow - ['customer', 'product']. but i take here all.


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
