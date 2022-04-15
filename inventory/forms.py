from ast import Delete
from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms import BaseInlineFormSet
from .models import Ingredient, MenuItem, Menu, Order, IngredientQuantity

class InventoryCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'

class MenuCreateForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'

class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price']

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer',]

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']