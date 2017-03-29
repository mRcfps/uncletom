from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, CreateView, DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Shop, Food, Order, Comment
from .forms import NewShopForm
from common import orderoperators


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

    def get_queryset(self):
        self.shop = Shop.objects.get(pk=self.kwargs['shop_id'])
        return self.shop.food_set.all()

    def get_context_data(self, **kwargs):
        ctx = super(ShopDetailView, self).get_context_data(**kwargs)
        ctx['shop'] = self.shop
        ctx['comments'] = Comment.objects \
            .filter(shop=self.shop).order_by('-add_time')

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
        orderoperators.create_order(request)
        return render(request, 'market/pay_success.html')


class MyOrdersView(TemplateView):
    template_name = 'market/my_orders.html'

    def get_context_data(self, **kwargs):
        ctx = super(MyOrdersView, self).get_context_data(**kwargs)

        ctx['paid_orders'], ctx['accepted_orders'], ctx['finished_orders'] = \
            orderoperators.fetch_orders_for_customer(self.request)

        return ctx


class FinishOrderView(View):
    def get(self, request, order_id):
        orderoperators.finish_order(request, order_id)
        context = {'order': Order.objects.get(id=order_id)}

        return render(request, 'market/comment.html', context)


class CommentView(View):
    def get(self, request, order_id):
        context = {
            'order': Order.objects.get(id=order_id),
            'has_commented': True,
        }
        return render(request, 'market/comment.html', context)

    def post(self, request, order_id):
        new_comment = Comment()
        new_comment.customer = request.user
        new_comment.shop = Order.objects.get(id=order_id).get_seller()
        new_comment.body = request.POST['body']
        new_comment.save()

        context = {
            'order': Order.objects.get(id=order_id),
            'has_commented': True,
        }

        return render(request, 'market/comment.html', context)
