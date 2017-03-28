from django.db import models

from django.contrib.auth.models import User


class Shop(models.Model):
    owner = models.ForeignKey(User, related_name='shop')

    name = models.CharField(max_length=50)
    sale_num = models.IntegerField(default=0)
    rating = models.FloatField(default=5.0)
    logo = models.ImageField(upload_to='img')

    def __str__(self):
        return self.name


class Food(models.Model):
    seller = models.ForeignKey(Shop)

    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    sale_num = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='img')

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User)
    food_list = models.ManyToManyField(Food)

    STATUS_CHOICE = (
        ('paid', '已付款'),
        ('accepted', '商家已接单'),
        ('finished', '订单已完成'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICE,
        default='paid',
    )
    time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    food = models.ForeignKey(Food)
    customer = models.ForeignKey(User)

    body = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return customer + "'s comment on " + food
