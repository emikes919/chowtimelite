from django.contrib import admin
from .models import Ingredient, MenuItem, Menu, Order, IngredientQuantity

admin.site.register(Ingredient)
admin.site.register(MenuItem)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(IngredientQuantity)