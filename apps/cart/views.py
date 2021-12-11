from django.contrib.messages.api import error
import stripe
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib import messages
from .forms import CheckoutForm
from .cart import Cart
from apps.order.utilities import Checkout, notify_customer, notify_seller

def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form  = CheckoutForm(request.POST)

        if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token'] # takes stripe token for pruchase
            try:
                charge = stripe.Charge.create(amount = int(cart.get_total_cost()*100), 
                currency = 'USD', description = 'Charge from Bernard', source = stripe_token) #returns the charge amount for purchases that will be transfered to stripe interface
#accounts for all data needed for order *requred*
                firstName = form.cleaned_data['firstName']
                lastName = form.cleaned_data['lastName']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                area = form.cleaned_data['area']
                pNumber = form.cleaned_data['pNumber']

                order = Checkout(request, firstName,lastName,email,address,zipcode,area,pNumber, cart.get_total_cost()) #shared data for order checkout
                #free up saved memory for cart
                cart.clear()
                notify_seller(order) #sends out https request for the seller of bought item from email
                notify_customer(order)#sends out https request for the buyer of bought item from email
                return redirect('success')#sucessful output
            except Exception:
                messages.error(request, "Payment Error Occured, try again later")
    else:
        form = CheckoutForm()


    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart: # get request to delete items from cart
        cart.remove(remove_from_cart)

        return redirect('cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)
        
        return redirect('cart')

    return render(request, 'cart.html',{'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY}) #return the render of the cart with data updated and stripe func

def success(request):
    return render(request, 'success.html')