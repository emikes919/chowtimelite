from django.db import models
from django.contrib.auth.models import User
import datetime

class Ingredient(models.Model):
    GRAM = 'Grams'
    OUNCE = 'Ounces'
    PIECE = 'Pieces'

    UNIT_CHOICES = [
        ('Grams', 'Grams'),
        ('Ounces', 'Ounces'),
        ('Pieces', 'Pieces')
    ]

    '''
    users: 
    - on_delete=models.SET_NULL so if the user is deleted, the ingredient model instances aren't deleted as well 
    - null=True since we already have database data and we couldn't migrate without having to add a default
    '''
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    name = models.CharField(max_length=200)
    unitType = models.CharField(max_length=200, choices=UNIT_CHOICES, verbose_name='Unit')
    unitCost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Unit Cost')
    inventoryQuantity = models.IntegerField(default=0, verbose_name='Quantity')

    def __str__(self):
        return self.name

    def totalCost(self):
        result = self.inventoryQuantity * self.unitCost
        return "${:,.0f}".format(result)

class Menu(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    name = models.CharField(max_length=200)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class MenuItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientQuantity')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def itemCost(self):
        relevantIngredients = IngredientQuantity.objects.filter(menuItem=self)
        cost = 0

        for ingredient in relevantIngredients:
            cost += (ingredient.ingredient.unitCost * ingredient.ingredientQuantity)

        return cost

class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredientQuantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.ingredient)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    menuItems = models.ManyToManyField(MenuItem, through='DishQuantity')
    timestamp = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=200)

    def __str__(self):
        return 'Order #' + str(self.id)

    def getDishQuantities(self):
        quantities = DishQuantity.objects.filter(order=self)
        return quantities

    def revenue(self):
        selectedDishes = DishQuantity.objects.filter(order=self)
        revenue = 0

        for dish in selectedDishes:
            revenue += (dish.menuItem.price * dish.dishQuantity)
        
        return revenue
    
    def COGS(self):
        selectedDishes = DishQuantity.objects.filter(order=self)
        cogs = 0

        for dish in selectedDishes:
            cogs = (dish.menuItem.itemCost() * dish.dishQuantity)
        
        return cogs

class DishQuantity(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    dishQuantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.order) + ' - ' + str(self.menuItem)