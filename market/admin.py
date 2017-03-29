from django.contrib import admin

from .models import Shop, Food, Order, Comment


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'time', 'show_food_list', 'status')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'add_time', 'customer', 'shop')


admin.site.register(Shop)
admin.site.register(Food)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment, CommentAdmin)
