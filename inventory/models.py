from django.db import models
import datetime

class Ingredient(models.Model):
    GRAM = 'GR'
    OUNCE = 'OZ'
    ITEM = 'IT'

    UNIT_CHOICES = [
        ('GR', 'Grams'),
        ('OZ', 'Ounces'),
        ('IT', 'Item')
    ]

    name = models.CharField(max_length=200)
    unitType = models.CharField(max_length=200, choices=UNIT_CHOICES, default=ITEM)
    unitCost = models.DecimalField(max_digits=10, decimal_places=2)
    inventoryQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name + ' (' + self.unitType + ')'

    def totalCost(self):
        result = self.inventoryQuantity * self.unitCost
        return "{:.0f}".format(result)

class Menu(models.Model):
    name = models.CharField(max_length=200)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class MenuItem(models.Model):
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