from django.views.generic import \
    View, CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from market.models import Food, Order
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
    model = Food
    fields = ['name', 'price', 'photo']

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


class UpdateFoodView(UpdateView):
    template_name = 'shop_manager/update_food.html'
    model = Food
    fields = ['name', 'price', 'photo']
    success_url = reverse_lazy('shop_manager:shop-manage')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        food = Food.objects.get(id=self.kwargs['pk'])
        if food.seller != self.request.user.shop:
            # The food does not belong to the current user's shop in which
            # case we will block his/her request
            raise Http404
        else:
            return super(UpdateFoodView, self).dispatch(*args, **kwargs)


class DeleteFoodView(DeleteView):
    template_name = 'shop_manager/food_confirm_delete.html'
    model = Food
    success_url = reverse_lazy('shop_manager:shop-manage')


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
        if order.get_seller() != self.request.user.shop:
            # This order does not belong to the current shop in which
            # case we will block his/her request
            raise Http404
        else:
            return super(AcceptOrderView, self).dispatch(*args, **kwargs)

    def get(self, request, order_id):
        orderoperators.accept_order(request, order_id)

        return HttpResponseRedirect(reverse('shop_manager:order-management'))
