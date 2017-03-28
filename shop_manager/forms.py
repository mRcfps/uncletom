from django import forms

from market.models import Food


class NewFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'price', 'photo']
        labels = {
            'name': '名称',
            'price': '价格',
            'photo': '图片',
        }
