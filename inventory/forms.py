from ast import Delete
from tabnanny import verbose
from tkinter import W, Widget
from tkinter.tix import Select
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms import inlineformset_factory
from .models import Ingredient, MenuItem, Menu, Order, IngredientQuantity, DishQuantity

class InventoryCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'add-edit-form-input'}))
    unitType = forms.ChoiceField(widget=forms.Select(attrs={'class': 'add-edit-form-input'}), choices=Ingredient.UNIT_CHOICES)
    unitCost = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'add-edit-form-input'}), decimal_places=2, min_value=0.01)
    inventoryQuantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'add-edit-form-input'}), min_value=1)

    class Meta:
        model = Ingredient
        fields = '__all__'

class MenuCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'add-edit-form-input'}))
    
    class Meta:
        model = Menu
        fields = '__all__'

class ItemCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'add-edit-form-input'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'add-edit-form-input'}), decimal_places=2, min_value=0.01)

    class Meta:
        model = MenuItem
        fields = ['name', 'price']

class OrderCreateForm(forms.ModelForm):
    customer = forms.CharField(widget=forms.TextInput(attrs={'class': 'add-edit-form-input'}))
    
    class Meta:
        model = Order
        fields = ['customer',]

class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-field-input'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-field-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-field-input', 'placeholder': ' Create a password...'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-field-input', 'placeholder': ' Re-enter your password...'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ItemIngredientForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].queryset = Ingredient.objects.filter(user=self.user)

    ingredient = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'add-edit-form-input'}), queryset=Ingredient.objects.all(), empty_label="Select an ingredient...")
    ingredientQuantity = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'add-item-dynamic-quantity-form-input'}), min_value=.01, decimal_places=2)

IngredientQuantityFormset = inlineformset_factory(
    MenuItem, IngredientQuantity, form=ItemIngredientForm, fields=('ingredient', 'ingredientQuantity'), can_delete=True, extra=0
)

class OrderDishForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['menuItem'].queryset = MenuItem.objects.filter(user=self.user)
    
    menuItem = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'add-edit-form-input'}), queryset=MenuItem.objects.all(), empty_label="Select a dish...")
    dishQuantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'add-item-dynamic-quantity-form-input'}), min_value=1)

DishQuantityFormset = inlineformset_factory(
    Order, DishQuantity, form=OrderDishForm, fields=('menuItem', 'dishQuantity'), can_delete=True, extra=0
)