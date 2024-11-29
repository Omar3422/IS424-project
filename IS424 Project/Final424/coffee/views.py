from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import MenuItem, Purchase
from .forms import UserForm, SignupForm, MenuItemForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

@login_required
def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, "coffee/menu.html", {"menu_items": menu_items})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("coffee:menu"))
        else:
            return render(request, "coffee/signup.html", {"form": form})
    return render(request, "coffee/signup.html", {"form": SignupForm()})

def login(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse("coffee:menu"))
            else:
                return render(request, "coffee/login.html", {"form": form, "error": "Invalid credentials"})
        else:
            return render(request, "coffee/login.html", {"form": form})
    return render(request, "coffee/login.html", {"form": UserForm()})

@login_required
def add_menu_item(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("coffee:menu"))
    else:
        form = MenuItemForm()
    return render(request, "coffee/add_menu_item.html", {"form": form})

@login_required
def item_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        purchase, created = Purchase.objects.get_or_create(user=request.user, item=item)
        if not created:
            purchase.quantity += quantity
        purchase.save()
        return redirect('coffee:item_detail', pk=pk)

    purchases = Purchase.objects.filter(item=item).select_related('user')
    return render(request, 'coffee/item_detail.html', {
        'item': item,
        'purchases': purchases,
    })

@login_required
def item_update(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('coffee:item_detail', pk=pk)
    else:
        form = MenuItemForm(instance=item)
    return render(request, "coffee/item_form.html", {"form": form})