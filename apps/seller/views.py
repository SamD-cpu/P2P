from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Seller
from apps.item.models import Item

from django.utils.text import slugify
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ItemForm

# Create your views here.
def SignupSeller(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save() #saves the data for the forms of data used in item

            login(request, user)

            seller = Seller.objects.create(name = user.username, created_by = user)#seller object created with the inherited qualities of items

            return redirect('frontpage')

    else:
        form = UserCreationForm()

    return render(request, 'seller/SignupSeller.html', {'form': form})

@login_required
def SellerAdmin(request):
    #all values for 
    seller = request.user.seller
    items = seller.items.all()
    orders = seller.orders.all()

    for order in orders:
        order.seller_amount = 0
        order.seller_paid_amount = 0
        order.fully_paid = True

        for item in order.item.all():
            if item.seller == request.user.seller:#updates seller cost and paid for...
                if item.sellerCheck:
                    order.seller_paid_amount += item.get_total_cost()
                else:
                    order.seller_amount += item.get_total_cost()
                    order.fully_paid = False

    return render(request, 'seller/SellerAdmin.html', {'seller': seller, 'items': items, 'orders': orders})


@login_required
def AddItem(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)#get item forms for listing to add

        if form.is_valid():
            item = form.save(commit=False)#saves form
            item.seller = request.user.seller#seller reqest
            item.slug = slugify(item.title)#url title
            item.save()

            return redirect('SellerAdmin')
    else:
        form = ItemForm()

    return render(request, 'seller/AddItem.html', {'form' : form})


def EditItem(request, pk):
    seller = request.user.seller
    item = seller.items.get(pk = pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance= item)#obtain instance for updating
        if form.is_valid():
            form.save()

            return redirect('SellerAdmin')
    
    else:
        form = ItemForm(instance= item)
    
    return render(request, 'seller/AddItem.html', {'form' : form, 'item': item})#changes for data


@login_required
def Edit(request):
    seller = request.user.seller

    if request.method == 'POST':
        name = request.POST.get('name','')#edits the name
        email = request.POST.get('email','')#edits the email 
        
        if name: 
            seller.created_by.email = email #new instance
            seller.created_by.save()

            seller.created_by.name = name#update instance
            seller.created_by.save()

            return redirect('SellerAdmin')
    return render(request, 'seller/edit.html', {'seller': seller})

def sellers(request):
    sellers = Seller.objects.all() #to list sellers

    return render(request, 'seller/sellers.html', {'sellers': sellers})

def seller(request, seller_id):
    seller = get_object_or_404(Seller, pk=seller_id)#seller info

    return render(request, 'seller/seller.html', {'seller': seller})