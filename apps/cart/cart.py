from django.conf import settings

from apps.item.models import Item

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID) #gets session that last for 24 max

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['item'] = Item.objects.get(pk=p) #gets the item and generates the list of 
        #items and returns a stream of data to be put into cart real time
        
        for item in self.cart.values():
            item['total_price'] = item['item'].price * item['quantity'] #gets values of item object in the cart

            yield item #returns the item list with allocated values
    
    def __len__(self): #method in place for object item #length in cart
        return sum(item['quantity'] for item in self.cart.values())
    
    def add(self, item_id, quantity=1, update_quantity=False):
        item_id = str(item_id)
        
        if item_id not in self.cart: #add unique item to cart
            self.cart[item_id] = {'quantity': 1, 'id': item_id}
        
        if update_quantity:
            self.cart[item_id]['quantity'] += int(quantity)

            if self.cart[item_id]['quantity'] == 0:
                self.remove(item_id)
                        
        self.save()
    
    def remove(self, item_id): #function to remove item from cart 
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart #saves value of cart
        self.session.modified = True #updates session so exact time of value
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID] #session delete func
        self.session.modified = True
    
    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['item'] = Item.objects.get(pk=p)

        return sum(item['quantity'] * item['item'].price for item in self.cart.values())