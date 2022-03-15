from django.db import models

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
    unitType = models.CharField(max_length=2, choices=UNIT_CHOICES, default=ITEM)
    unitCost = models.DecimalField(max_digits=10, decimal_places=2)
    inventoryQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

    def totalCost(self):
        result = self.inventoryQuantity * self.unitCost
        return "{:.0f}".format(result)

class Menu(models.Model):
    name = models.CharField(max_length=200)
    timeCreated = models.DateTimeField(auto_now=True)
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

class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredientQuantity = models.IntegerField(default=0)

    # class Meta:
    #     unqiue_together = ('ingredient', 'menuItem')

    def __str__(self):
        return str(self.ingredient)

class Order(models.Model):
    menuItem = models.ManyToManyField(MenuItem)
    timestamp = models.DateTimeField(auto_now=True)
    customer = models.CharField(max_length=200)
    
    # def revenue(self):
    #     price = self.menuItem.price
    #     return price * self.dishQuantity
    
    # def cost(self):
    #     cost = self.dish.cost
    #     return cost * self.dishQuantity