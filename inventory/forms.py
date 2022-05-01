from ast import Delete
from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms import inlineformset_factory
from .models import Ingredient, MenuItem, Menu, Order, IngredientQuantity, DishQuantity

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
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Create a username...'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address...'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Create a password...'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter your password...'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ItemIngredientForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].queryset = Ingredient.objects.filter(user=self.user)

    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), empty_label="Select an ingredient...")

IngredientQuantityFormset = inlineformset_factory(
    MenuItem, IngredientQuantity, form=ItemIngredientForm, fields=('ingredient', 'ingredientQuantity'), can_delete=True, extra=0
)

class OrderDishForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['menuItem'].queryset = MenuItem.objects.filter(user=self.user)
    
    menuItem = forms.ModelChoiceField(queryset=MenuItem.objects.all(), empty_label="Select a dish...")

DishQuantityFormset = inlineformset_factory(
    Order, DishQuantity, form=OrderDishForm, fields=('menuItem', 'dishQuantity'), can_delete=True, extra=0
)