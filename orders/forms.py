from django import forms

class OrderForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, initial=1, label="Количество")
    address = forms.CharField(max_length=300, label="Адрес доставки")
    phone = forms.CharField(max_length=20, label="Контактный телефон")
