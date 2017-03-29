from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, CreateView, DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Shop, Food, Order
from .forms import NewShopForm


class HomeView(ListView):
    template_name = 'market/home.html'
    model = Shop
    context_object_name = 'shops'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.user

        # check out whether the user has logged in and has a shop
        if user.is_authenticated and user.shop:
            ctx['has_shop'] = True
        else:
            ctx['has_shop'] = False

        return ctx


class NewShopView(CreateView):
    template_name = 'market/new_shop.html'
    form_class = NewShopForm

    def form_valid(self, form):
        new_shop = form.save(commit=False)
        new_shop.owner = self.request.user
        new_shop.save()

        return HttpResponseRedirect(reverse('market:home'))


class ShopDetailView(ListView):
    template_name = 'market/shop.html'
    context_object_name = 'foods'

    def get_shop(self):
        return Shop.objects.get(pk=self.kwargs['shop_id'])

    def get_queryset(self):
        return self.get_shop().food_set.all()

    def get_context_data(self, **kwargs):
        ctx = super(ShopDetailView, self).get_context_data(**kwargs)
        ctx['shop'] = self.get_shop()

        return ctx


class FoodDetailView(DetailView):
    template_name = 'market/food.html'
    model = Food
    context_object_name = 'food'

    def get_context_data(self, **kwargs):
        ctx = super(FoodDetailView, self).get_context_data(**kwargs)

        food = ctx['food']
        ctx['shop'] = food.seller
        ctx['comments'] = food.comment_set.all()

        return ctx


class CheckoutView(View):
    http_method_names = ('post', )

    def post(self, request):
        # get the food list from the posted food_id
        food_list = []
        for food_name, food_id in request.POST.items():
            if food_name != 'csrfmiddlewaretoken':
                food_list.append(Food.objects.get(pk=food_id))

        total_price = 0
        for food in food_list:
            total_price += food.price
        context = {'food_list': food_list, 'total_price': total_price}

        return render(request, 'market/order_detail.html', context)


class PayView(View):
    http_method_names = ('post', )

    def post(self, request):
        new_order = Order(customer=request.user, status='paid')
        new_order.save()

        shop = Shop()

        for food_name, food_id in request.POST.items():
            if food_name != 'csrfmiddlewaretoken':
                food = Food.objects.get(pk=food_id)
                shop = food.seller
                new_order.food_list.add(food)
                food.sale_num += 1
                food.save()

        shop.sale_num += 1
        shop.save()

        return render(request, 'market/pay_success.html')


class MyOrdersView(TemplateView):
    template_name = 'market/my_orders.html'

    def get_orders_with_sellers(self, orders):
        '''Return a list of orders, each attached with its seller'''
        order_list = []
        for order in orders:
            fake_order = {}
            fake_order['seller'] = order.food_list.all()[0].seller
            fake_order['food_list'] = list(order.food_list.all())
            fake_order['time'] = order.time
            order_list.append(fake_order)
        return order_list

    def get_context_data(self, **kwargs):
        ctx = super(MyOrdersView, self).get_context_data(**kwargs)

        # Get orders with status 'paid'
        paid_orders = Order.objects.filter(
            customer=self.request.user,
            status='paid',
        ).order_by('-time')

        # Get orders with status 'accepted'
        accepted_orders = Order.objects.filter(
            customer=self.request.user,
            status='accepted',
        ).order_by('-time')

        # Get orders with status 'finished'
        finished_orders = Order.objects.filter(
            customer=self.request.user,
            status='finished',
        ).order_by('-time')

        ctx['paid_orders'] = self.get_orders_with_sellers(paid_orders)
        ctx['accepted_orders'] = self.get_orders_with_sellers(accepted_orders)
        ctx['finished_orders'] = self.get_orders_with_sellers(finished_orders)

        return ctx
