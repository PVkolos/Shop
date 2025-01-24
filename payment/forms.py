from django import forms


class OrderForm(forms.Form):
    index = forms.CharField(max_length=20)
    link = forms.URLField()
