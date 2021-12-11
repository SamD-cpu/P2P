from PIL.Image import Image
from django.db import models
from io import BytesIO
from PIL import *
from django.core.files import File
from django.contrib.auth.models import User
from apps.seller.models import Seller
from django.db.models import Sum


from apps.seller.models import Seller

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField (
    verbose_name = "slug",
    allow_unicode = True,
    unique=True,
    blank = True,
    null = True)
    ordering = models.IntegerField(default=0)

    def __str__(self):
            return self.title

    class Meta:
        ordering = ['ordering']

        

class Item(models.Model):
    ITEM_SIZES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
    )
    category = models.ForeignKey(Category, related_name = "items", on_delete= models.CASCADE)
    seller = models.ForeignKey(Seller, related_name = "items", on_delete= models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField (
    verbose_name = "slug",
    allow_unicode = True,
    unique=True,
    blank = True,
    null = True)
    description = models.TextField(blank = True, null= True)
    price = models.DecimalField(max_digits=6, decimal_places = 2)
    item_size = models.CharField(max_length= 3, choices= ITEM_SIZES)
    Brand = models.TextField(max_length= 50, blank = True, null = True)
    color = models.TextField(max_length= 20, blank= True, null= True)
    condition = models.TextField(max_length= 15, blank = True, null = True)
    date_added = models.DateTimeField(auto_now_add= True)
    image1 = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    image2 = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    image3 = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    image4 = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
    thumbnail = models.ImageField(upload_to = 'uploads/', blank = True, null = True)
        
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_added']

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image1:
                self.thumbnail = self.make_thumbnail(self.image1)
                self.save()
  
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'

    def make_thumbnail(self, image, size = (300,200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality = 100)

        thumbnail = File(thumb_io, name = image.name)

        return thumbnail
        
    def get_rating(self):
        try:
            total = 0
            total = sum(int(review['stars'])for review in self.review.values())
            return (total / (self.review.count()))
        except ZeroDivisionError:
            total = 0


class Review(models.Model):
    user = models.ForeignKey(Seller, related_name= 'review', on_delete = models.CASCADE)
    item = models.ForeignKey(Item, related_name= 'review', on_delete = models.CASCADE )
    content = models.TextField(max_length=255)
    stars = models.IntegerField(default= 0)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return str(self.seller.name)

    