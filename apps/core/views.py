from django.shortcuts import render

from apps.item.models import Item

def frontpage(request):
    newItems = Item.objects.all()
    return render(request, 'core/frontpage.html',{'newItems': newItems})

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')
    