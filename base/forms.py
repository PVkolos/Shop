from django import forms


class OrderForm(forms.Form):
    products = forms.CharField(max_length=400)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    values = forms.CharField(max_length=400)