from tkinter import Widget
from django import forms
from django.forms.models import inlineformset_factory
from .models import Ingredient, MenuItem, Menu, Order, IngredientQuantity

class InventoryCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'

class MenuCreateForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name']

class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price']
        # exclude = ['menu',]
    
    # ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), widget=forms.CheckboxSelectMultiple)
    # name = forms.CharField()
    # price = forms.DecimalField(decimal_places=2)

class IngredientQuantityForm(forms.ModelForm):
    class Meta:
        model = IngredientQuantity
        fields = '__all__'

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'