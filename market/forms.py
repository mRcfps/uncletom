from django import forms

from .models import Shop


class NewShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'logo']
        labels = {'name': '餐厅名字', 'logo': 'Logo'}


class OrderForm(forms.Form):
    pass
