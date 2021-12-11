from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Seller(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    created_by = models.OneToOneField(User, related_name = 'seller', on_delete = models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def getBalance(self):
        items = self.item.filter(sellerCheck = False, order__sellers__in=[self.id])
        return sum((item.item.price * item.quantity) for item in items)

    def getPaidCost(self):
        items = self.item.filter(sellerCheck = True, order__sellers__in=[self.id])
        return sum((item.item.price * item.quantity) for item in items)