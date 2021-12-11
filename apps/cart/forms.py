from django import forms

class CheckoutForm(forms.Form):
    firstName = forms.CharField(max_length=255)
    lastName = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
    area = forms.CharField(max_length=255)
    pNumber = forms.CharField(max_length=255)
    stripe_token = forms.CharField(max_length=255)