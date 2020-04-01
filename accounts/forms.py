from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm): # name of the model and Form. and inherit from ModelForm.
    class Meta:
        model = Order # which model
        fields = '__all__' # which fields i will allow - ['customer', 'product']. but i take here all.
