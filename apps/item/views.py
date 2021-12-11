from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, query
import random
from .models import Category, Item, Review
from .forms import ItemAddForm
from apps.cart.cart import Cart
from django.contrib.auth.models import User

def search(request):
    query = request.GET.get('query', '')
    items = Item.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/parts/search.html', {'items': items, 'query': query})

def item(request, category_slug, item_slug):
    cart = Cart(request)
    item = get_object_or_404(Item, category__slug = category_slug, slug = item_slug)

    if request.method == 'POST':
        form = ItemAddForm(request.POST)
    
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            cart.add(item_id= item.id, quantity= quantity, update_quantity = False)

            messages.success(request, "Item added to cart")

            return redirect('item', category_slug= category_slug, item_slug=item_slug)
    else:
        form = ItemAddForm()

    similar_item = list(item.category.items.exclude(id = item.id))

    if request.method == 'POST' and request.user.is_authenticated:
                stars = request.POST.get('stars', 3)
                content = request.POST.get('content', '')
                review = Review.objects.create(item = item, user = item.seller, stars = stars, content = content)
                return redirect('item', category_slug = category_slug, item_slug = item_slug)

    if len(similar_item) >= 4: 
        similar_item = random.sample(similar_item, 4)
    
    return render(request, 'item/item.html', {'item': item, 'similar_item': similar_item})

def category(request, category_slug):
    category = get_object_or_404(Category, slug = category_slug)
        
    return render(request, 'item/parts/category.html', {'category': category})

