from django.forms import ModelForm
from apps.item.models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['category','title','slug','description','price','item_size','Brand','color'
        ,'condition','image1','image2','image3','image4','thumbnail']

