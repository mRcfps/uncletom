from django.contrib import admin

from .models import Shop, Food, Order, Comment

admin.site.register(Shop)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(Comment)
