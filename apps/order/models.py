from django.db import models
from apps.item.models import Item
from apps.seller.models import Seller

class Order(models.Model): #order information lateral to cart information 
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    pNumber = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add= True)
    paid_cost = models.DecimalField(max_digits= 8, decimal_places= 2)
    sellers = models.ManyToManyField(Seller, related_name='orders')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.firstName

class ItemOrder(models.Model):
    order = models.ForeignKey(Order, related_name='item', on_delete=models.CASCADE, default="") #order form item model
    item = models.ForeignKey(Item, related_name='item', on_delete=models.CASCADE, default="")#item from item model
    seller = models.ForeignKey(Seller, related_name= 'item', on_delete=models.CASCADE)#seller from seller model
    sellerCheck = models.BooleanField(default=False)#checks if the seller is paid or not
    price = models.DecimalField(max_digits=8, decimal_places = 2)
    quantity = models.IntegerField(default = 1)#value quantity 

    def __str__(self):
        return str(self.id)
    
    def get_total_cost(self):
        return self.price * self.quantity