from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from pprint import pprint
import json

from .models import Ingredient, IngredientQuantity, MenuItem, Menu, Order, DishQuantity
from .forms import InventoryCreateForm, MenuCreateForm, ItemCreateForm, OrderCreateForm, CreateUserForm

def landingPage(request):
    return render(request, 'inventory/landingPage.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for %s' % (user))
                return redirect('login')
        
        context = {'form': form}
        return render(request, 'inventory/register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect.')

        context = {}
        return render(request, 'inventory/login.html', context)  

def logoutView(request):
    logout(request)
    return redirect('landingpage')

@login_required(login_url='login')
def Home(request):
    return render(request, 'inventory/home.html')

@login_required(login_url='login')
def InventoryList(request):
    inventory = Ingredient.objects.all()
    context = {'inventory': inventory}
    return render(request, 'inventory/inventoryList.html', context)

@login_required(login_url='login')
def InventoryCreate(request):
    form = InventoryCreateForm()

    if request.method == 'POST':
        form = InventoryCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventorylist')

    context = {'form': form}
    return render(request, 'inventory/inventoryCreate.html', context)

@login_required(login_url='login')
def InventoryUpdate(request, pk):
    inventory = Ingredient.objects.get(id=pk)
    form = InventoryCreateForm(instance=inventory)

    if request.method == 'POST':
        form = InventoryCreateForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            return redirect('inventorylist')
    
    context = {'form': form, 'inventory': inventory}
    return render(request, 'inventory/inventoryEdit.html', context)

@login_required(login_url='login')
def InventoryDelete(request, pk):
    inventory = Ingredient.objects.get(id=pk)
    if request.method == 'POST':
        inventory.delete()
        return redirect('inventorylist')
    
    return render(request, 'inventory/inventoryDelete.html', {'obj': inventory})

@login_required(login_url='login')
def MenuList(request):
    menus = Menu.objects.all()
    context = {'menus': menus}
    return render(request, 'inventory/menuList.html', context)

@login_required(login_url='login')
def MenuCreate(request):
    form = MenuCreateForm

    if request.method == 'POST':
        form = MenuCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menulist')
    
    context = {'form': form}
    return render(request, 'inventory/menuCreate.html', context)

@login_required(login_url='login')
def MenuView(request, pk):
    menu = Menu.objects.get(id=pk)
    items = MenuItem.objects.filter(menu=menu)
    context = {'menu': menu, 'items': items}
    return render(request, 'inventory/menuView.html', context)

@login_required(login_url='login')
def MenuUpdate(request, pk):
    menu = Menu.objects.get(id=pk)
    form = MenuCreateForm(instance=menu)

    if request.method == 'POST':
        form = MenuCreateForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('menulist')
    
    context = {'form': form, 'menu': menu}
    return render(request, 'inventory/menuUpdate.html', context)

@login_required(login_url='login')
def MenuDelete(request, pk):
    menu = Menu.objects.get(id=pk)
    if request.method == 'POST':
        menu.delete()
        return redirect('menulist')
    
    return render(request, 'inventory/menuDelete.html', {'obj': menu})

@login_required(login_url='login')
def ItemCreate(request, pk):
    # how I did this:
    # https://stackoverflow.com/questions/8971606/how-to-set-foreign-key-during-form-completion-python-django
    
    menu = Menu.objects.get(id=pk)
    form = ItemCreateForm()

    if request.method == 'POST':
        form = ItemCreateForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.menu = menu
            item.save()
            # form.save_m2m()
            return redirect('menuview', menu.id)

    context = {'form': form, 'menu': menu}
    return render(request, 'inventory/itemCreate.html', context)

@login_required(login_url='login')
def ItemUpdate(request, pk):
    item = MenuItem.objects.get(id=pk)

    IngredientQuantityFormset = inlineformset_factory(
        MenuItem, IngredientQuantity, fields=('ingredient', 'ingredientQuantity'), can_delete=True, extra=0
    )
    formset = IngredientQuantityFormset(instance=item)
    form = ItemCreateForm(instance=item)

    if request.method == 'POST':
        pprint('request.POST :')
        pprint(request.POST)
        form = ItemCreateForm(request.POST, instance=item)
        formset = IngredientQuantityFormset(request.POST, instance=item)
        print('form valid?')
        print(form.is_valid())
        print('formset valid')
        print(formset.is_valid())
        print('formset errors')
        print(formset.errors)
        if (form.is_valid() and formset.is_valid()):
            form.save()
            formset.save()
            return redirect('menuview', item.menu.id)
    
    context = {'form': form, 'formset': formset, 'item': item}
    return render(request, 'inventory/itemEdit.html', context)

@login_required(login_url='login')
def ItemDelete(request, pk):
    item = MenuItem.objects.get(id=pk)
    
    if request.method == 'POST':
        item.delete()
        return redirect('menuview', item.menu.id)
    
    return render(request, 'inventory/itemDelete.html', {'obj': item})

@login_required(login_url='login')
def OrderList(request):
    orders = Order.objects.all()
    totalRevenue = 0

    for order in orders:
        totalRevenue += order.revenue()

    context = {'orders': orders, 'totalrevenue': totalRevenue}
    return render(request, 'inventory/orderList.html', context)

@login_required(login_url='login')
def OrderCreate(request):
    DishQuantityFormset = inlineformset_factory(
        Order, DishQuantity, fields=('menuItem', 'dishQuantity'), can_delete=True, extra=0
    )
    
    form = OrderCreateForm
    formset = DishQuantityFormset()
    
    error = False
    error_messages = {}
    dishLIST = []

    if request.method == 'POST':
        print('request.POST :')
        print(request.POST)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            
            formset = DishQuantityFormset(request.POST, instance=order)
            if formset.is_valid():
                ingredientDICT = {}

                for f in formset:
                    formData = f.cleaned_data # grab underlying data from the form
                    print('formData is: ')
                    print(formData)


                    dish = formData['menuItem']
                    dish_name = dish.name
                    dishLIST.append(dish_name) # make a list of each dish name in the order
                    menuItem = MenuItem.objects.get(name=dish) # grab the MenuItem DB object based on menuItem in form
                    
                    # loop through ingredients in that MenuItem to populate blank dict
                    for ingredient in IngredientQuantity.objects.filter(menuItem=menuItem): 
                        
                        # check if ingredient is already in blank dict to prevent overwriting, else map name and quantity to dict as k, v pair 
                        name = ingredient.ingredient.name
                        ingredient_quantity_per_dish = ingredient.ingredientQuantity
                        dish_quantity = formData['dishQuantity']
                        total_quantity_requirement = ingredient_quantity_per_dish * dish_quantity
                        
                        if name in ingredientDICT.keys():
                            ingredientDICT[name] = ingredientDICT[name] + total_quantity_requirement
                        else:
                            ingredientDICT[name] = total_quantity_requirement

                        # run validation logic - error message list populated if not enough inventory is available
                        ingredient_object_to_check = Ingredient.objects.get(name=name)
                        current_quantity = ingredient_object_to_check.inventoryQuantity
                        unit = ingredient_object_to_check.unitType
                        
                        if current_quantity < total_quantity_requirement:
                            error = True
                            error_message = f'Not enough inventory. You have {current_quantity} {unit} of {name} left.'
                            error_messages[dish_name] = error_message

                print('ingredient DICT:')
                pprint(ingredientDICT)
                
                print('dishLIST:')
                pprint(dishLIST)

                print('ERROR LIST:')
                print(error_messages)
                
                # check if an error has been triggered, if not update the DB and redirect
                if not error:
                    for i in ingredientDICT.keys(): # loop through the ingredients themselves to gather what we need to adjust the DB
                        ingredient_to_adjust = Ingredient.objects.get(name=i)
                        ingredient_to_adjust.inventoryQuantity -= ingredientDICT[i]
                        ingredient_to_adjust.save()
                    formset.save()
                    return redirect('orderlist')

    dishLIST = json.dumps(dishLIST)
    error_messages = json.dumps(error_messages)
    context = {'form': form, 'formset': formset, 'error': error, 'error_messages': error_messages, 'dishLIST': dishLIST}
    return render(request, 'inventory/orderCreate.html', context)

@login_required(login_url='login')
def OrderUpdate(request, pk):
    order = Order.objects.get(id=pk)
    DishQuantityFormset = inlineformset_factory(
        Order, DishQuantity, fields=('menuItem', 'dishQuantity'), can_delete=True, extra=0
    )
    
    form = OrderCreateForm(instance=order)
    formset = DishQuantityFormset(instance=order)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, instance=order)
        formset = DishQuantityFormset(request.POST, instance=order)
        if form.is_valid():
            form.save()
            formset.save()
            return redirect('orderlist')
    
    context = {'order': order, 'form': form, 'formset': formset}
    return render(request, 'inventory/orderEdit.html', context)

@login_required(login_url='login')
def OrderDelete(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('orderlist')
    
    return render(request, 'inventory/orderDelete.html', {'obj': order.id})

@login_required(login_url='login')
def pnlView(request):
    orders = Order.objects.all()
    orderdict = {}

    # grab every unique date 
    for order in orders:
        orderdict[order.timestamp.date()] = {}
    
    def getRevenueFromOrders(orderlist):
        revenue = 0
        for order in orderlist:
            revenue += order.revenue()
        return revenue

    def getCOGSFromOrders(orderlist):
        cogs = 0
        for order in orderlist:
            cogs += order.COGS()
        return cogs

    # populate value dicts for date keys with revenue, COGS, and GP for that date
    for orderdate in orderdict.keys():
        orderdict[orderdate]['revenue'] = getRevenueFromOrders(Order.objects.filter(timestamp__year=orderdate.year,
                                                                                    timestamp__month=orderdate.month,
                                                                                    timestamp__day=orderdate.day))
        orderdict[orderdate]['COGS'] = getCOGSFromOrders(Order.objects.filter(timestamp__year=orderdate.year,
                                                                              timestamp__month=orderdate.month,
                                                                              timestamp__day=orderdate.day))
        orderdict[orderdate]['GPdollar'] = orderdict[orderdate]['revenue'] - orderdict[orderdate]['COGS']
        orderdict[orderdate]['GPpct'] = '{:0.1%}'.format(orderdict[orderdate]['GPdollar'] / orderdict[orderdate]['revenue'])

    # calc subtotals of revenue, COGS, and GP
    totalRevenue = 0
    totalCOGS = 0

    for v in orderdict.values():
        totalRevenue += v['revenue']
        totalCOGS += v['COGS']

    totalGPdollar = totalRevenue - totalCOGS
    totalGPpct = '{:0.1%}'.format(totalGPdollar / totalRevenue)

    pprint(orderdict)

    context = {'orderdict': orderdict, 'totalRevenue': totalRevenue, 'totalCOGS': totalCOGS, 'totalGPdollar': totalGPdollar, 'totalGPpct': totalGPpct}
    return render(request, 'inventory/pnlView.html', context)