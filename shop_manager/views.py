from django.views.generic import View, CreateView, TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from market.models import Order
from .forms import NewFoodForm
from common import orderoperators


class ShopManageView(TemplateView):
    template_name = 'shop_manager/shop_manage.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ShopManageView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ShopManageView, self).get_context_data(**kwargs)
        ctx['shop'] = self.request.user.shop
        ctx['foods'] = ctx['shop'].food_set.all()

        return ctx


class NewFoodView(CreateView):
    template_name = 'shop_manager/new_food.html'
    form_class = NewFoodForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewFoodView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        new_food = form.save(commit=False)
        new_food.seller = self.request.user.shop
        new_food.save()

        return HttpResponseRedirect(reverse('shop_manager:shop-manage'))

    def get_context_data(self, **kwargs):
        ctx = super(NewFoodView, self).get_context_data(**kwargs)
        ctx['shop'] = self.request.user.shop

        return ctx


class OrderManagementView(TemplateView):
    template_name = 'shop_manager/order_management.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrderManagementView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(OrderManagementView, self).get_context_data(**kwargs)
        ctx['shop'] = self.request.user.shop
        ctx['new_orders'], ctx['accepted_orders'], ctx['finished_orders'] \
            = orderoperators.fetch_orders_for_shop(self.request)

        return ctx


class AcceptOrderView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs['order_id'])
        if order.get_seller() != self.request.user:
            # This order does not belong to the current user in which
            # case we will block his/her request
            raise Http404
        else:
            return super(AcceptOrderView, self).dispatch(*args, **kwargs)

    def get(self, request, order_id):
        orderoperators.accept_order(request, order_id)

        return HttpResponseRedirect(reverse('shop_manager:order-management'))
