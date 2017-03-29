from django.views.generic import View, CreateView, TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

from market.models import Order
from .forms import NewFoodForm


class ShopManageView(TemplateView):
    template_name = 'shop_manager/shop_manage.html'

    def get_context_data(self, **kwargs):
        ctx = super(ShopManageView, self).get_context_data(**kwargs)
        ctx['shop'] = self.request.user.shop
        ctx['foods'] = ctx['shop'].food_set.all()

        return ctx


class NewFoodView(CreateView):
    template_name = 'shop_manager/new_food.html'
    form_class = NewFoodForm

    def form_valid(self, form):
        new_food = form.save(commit=False)
        new_food.seller = self.request.user.shop.get()
        new_food.save()

        return HttpResponseRedirect(reverse('shop_manager:shop-manage'))

    def get_context_data(self, **kwargs):
        ctx = super(NewFoodView, self).get_context_data(**kwargs)
        ctx['shop'] = self.request.user.shop

        return ctx


def fetch_orders(request):
    '''Helps to fetch orders with different status of one shop'''
    shop = request.user.shop

    new_orders = Order.objects.filter(
        food_list__seller__name=shop.name,
        status='paid',
    ).distinct().order_by('-time')

    accepted_orders = Order.objects.filter(
        food_list__seller__name=shop.name,
        status='accepted',
    ).distinct().order_by('-time')

    finished_orders = Order.objects.filter(
        food_list__seller__name=shop.name,
        status='finished',
    ).distinct().order_by('-time')

    return new_orders, accepted_orders, finished_orders


class OrderManagementView(TemplateView):
    template_name = 'shop_manager/order_management.html'

    def get_context_data(self, **kwargs):
        ctx = super(OrderManagementView, self).get_context_data(**kwargs)
        ctx['shop'] = self.request.user.shop
        ctx['new_orders'], ctx['accepted_orders'], ctx['finished_orders'] \
            = fetch_orders(self.request)

        return ctx


class AcceptOrderView(View):
    def get(self, request, order_id):
        order = Order.objects.get(id=self.kwargs['order_id'])
        order.status = 'accepted'
        order.save()

        ctx = {'shop': request.user.shop}
        ctx['new_orders'], ctx['accepted_orders'], ctx['finished_orders'] \
            = fetch_orders(self.request)

        return render(request, 'shop_manager/order_management.html', ctx)
