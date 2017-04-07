from django.contrib import admin

from .models import Shop, Food, Order, Comment


class ShopAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'sale_num', 'logo')


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'price', 'sale_num', 'photo')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'time', 'show_food_list', 'status', 'has_commented')
    list_filter = ('customer', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'add_time', 'customer', 'shop')


admin.site.register(Shop, ShopAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment, CommentAdmin)
