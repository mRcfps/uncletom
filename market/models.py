from django.db import models

from django.contrib.auth.models import User


class Shop(models.Model):
    owner = models.OneToOneField(User)

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

    def show_food_list(self):
        '''A method to fetch the food list and return a string,
        used in OrderAdmin in this project.'''
        result = ''
        for food in self.food_list.all():
            result += food.name + ' '
        return result.rstrip()

    def get_seller(self):
        '''A shortcut method to know this order's seller
        without bringing redundancy to the database schema'''
        return self.food_list.all()[0].seller

    def __str__(self):
        return "{}'s order on {}".format(self.customer, self.time)


class Comment(models.Model):
    food = models.ForeignKey(Food)
    customer = models.ForeignKey(User)

    body = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return customer + "'s comment on " + food
