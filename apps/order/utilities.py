from apps.cart.cart import Cart
from .models import ItemOrder, Order 

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def Checkout(request, firstName, lastName, email, address, zipcode, area, pNumber, cost):#order object with same vars for cart order
    order = Order.objects.create(firstName = firstName, lastName = lastName, email = email, address = address, zipcode = zipcode, area = area, pNumber = pNumber, paid_cost = cost )

    for item in Cart(request):
        ItemOrder.objects.create(order = order, item = item['item'], seller = item['item'].seller, price = item['item'].price, quantity = item['quantity'])
        order.sellers.add(item['item'].seller)
    return ItemOrder

def notify_seller(order): #using django mail function to send email to the seller for notifying user
    fromEmail = settings.DEFAULT_EMAIL_FROM

    for seller in order.sellers.all():
        toEmail = seller.created_by.email
        subject = 'Order in Process'
        text_content = 'Check Seller Dashboard for order information'
        html_content = render_to_string('order/email_notify_seller.html', {'order': order, 'seller': seller})#takes the html format and redners it into a text format for sender

        msg = EmailMultiAlternatives(subject, text_content, fromEmail, [toEmail])#message in text format with typical preqto send
        msg.attach_alternative(html_content, 'text/html')#attachment for alt behaviors
        msg.send()#action

def notify_customer(order):# using django mail function to send email to the seller for notifying user
    fromEmail = settings.DEFAULT_EMAIL_FROM

    toEmail = order.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, fromEmail, [toEmail])#message in text format with typical preqto send
    msg.attach_alternative(html_content, 'text/html')#attachment for alt behaviors
    msg.send()#action