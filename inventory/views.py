from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .models import Ingredient, IngredientQuantity, MenuItem, Menu, Order
from .forms import InventoryCreateForm, MenuCreateForm, ItemCreateForm, OrderCreateForm, IngredientQuantityForm

def landingPage(request):
    return render(request, 'inventory/landingPage.html')

def Home(request):
    return render(request, 'inventory/home.html')

def InventoryList(request):
    inventory = Ingredient.objects.all()
    context = {'inventory': inventory}
    return render(request, 'inventory/inventoryList.html', context)

def InventoryCreate(request):
    form = InventoryCreateForm()

    if request.method == 'POST':
        form = InventoryCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventorylist')

    context = {'form': form}
    return render(request, 'inventory/inventoryCreate.html', context)

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

def InventoryDelete(request, pk):
    inventory = Ingredient.objects.get(id=pk)
    if request.method == 'POST':
        inventory.delete()
        return redirect('inventorylist')
    
    return render(request, 'inventory/inventoryDelete.html', {'obj': inventory})

def MenuList(request):
    menus = Menu.objects.all()
    context = {'menus': menus}
    return render(request, 'inventory/menuList.html', context)

def MenuCreate(request):
    form = MenuCreateForm

    if request.method == 'POST':
        form = MenuCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menulist')
    
    context = {'form': form}
    return render(request, 'inventory/menuCreate.html', context)

def MenuView(request, pk):
    menu = Menu.objects.get(id=pk)
    items = MenuItem.objects.filter(menu=menu)
    context = {'menu': menu, 'items': items}
    return render(request, 'inventory/menuView.html', context)

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

def MenuDelete(request, pk):
    menu = Menu.objects.get(id=pk)
    if request.method == 'POST':
        menu.delete()
        return redirect('menulist')
    
    return render(request, 'inventory/menuDelete.html', {'obj': menu})

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

def ItemUpdate(request, pk):
    item = MenuItem.objects.get(id=pk)

    IngredientQuantityFormset = inlineformset_factory(
        MenuItem, IngredientQuantity, fields=('ingredient', 'ingredientQuantity'), can_delete=False, extra=0
    )
    formset = IngredientQuantityFormset(instance=item)
    form = ItemCreateForm(instance=item)

    if request.method == 'POST':
        print('request.POST :')
        print(request.POST)
        form = ItemCreateForm(request.POST, instance=item)
        formset = IngredientQuantityFormset(request.POST, instance=item)
        if (form.is_valid() and formset.is_valid()):
            form.save()
            formset.save()
            print('item ingredients is:')
            print(item.ingredients)
            return redirect('menuview', item.menu.id)
    
    context = {'form': form, 'formset': formset, 'item': item}
    return render(request, 'inventory/itemEdit.html', context)

def ItemDelete(request, pk):
    item = MenuItem.objects.get(id=pk)
    
    if request.method == 'POST':
        item.delete()
        return redirect('menuview', item.menu.id)
    
    return render(request, 'inventory/itemDelete.html', {'obj': item})

def OrderList(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'inventory/orderList.html', context)

def OrderCreate(request):
    form = OrderCreateForm

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orderlist')
    
    context = {'form': form}
    return render(request, 'inventory/orderCreate.html', context)

def OrderUpdate(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderCreateForm(instance=order)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orderlist')
    
    context = {'order': order, 'form': form}
    return render(request, 'inventory/orderEdit.html', context)

def OrderDelete(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('orderlist')
    
    return render(request, 'inventory/orderDelete.html', {'obj': order.id})

def pnlView(request):
    return render(request, 'inventory/pnlView.html')