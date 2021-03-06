from django.db import models

from django.contrib.auth.models import User


class Shop(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, verbose_name='名称')
    sale_num = models.IntegerField(default=0, verbose_name='销量')
    rating = models.FloatField(default=5.0, verbose_name='评分')
    logo = models.ImageField(upload_to='img', verbose_name='商标')

    class Meta:
        verbose_name = '商家'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Food(models.Model):
    seller = models.ForeignKey(Shop, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, verbose_name='名称')
    price = models.FloatField(default=0, verbose_name='售价')
    sale_num = models.IntegerField(default=0, verbose_name='销量')
    photo = models.ImageField(upload_to='img', verbose_name='照片')

    class Meta:
        verbose_name = '美食'
        verbose_name_plural = verbose_name

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
    has_commented = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def show_food_list(self):
        """
        A method to fetch the food list and return a string,
        used in OrderAdmin in this project.
        """
        result = ''
        for food in self.food_list.all():
            result += food.name + ' '
        return result.rstrip()

    def get_seller(self):
        """
        A shortcut method to know this order's seller
        without bringing redundancy to the database schema
        """
        return self.food_list.all()[0].seller

    def __str__(self):
        return "{}'s order on {}".format(self.customer, self.time)


class Comment(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    body = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.customer) + "'s comment on " + str(self.shop)
