from django.views.generic import CreateView, TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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


class OrderManagementView(TemplateView):
    template_name = 'shop_manager/order_management.html'

    def get_context_data(self, **kwargs):
        ctx = super(OrderManagementView, self).get_context_data(**kwargs)

        shop = self.request.user.shop

        # Fetch orders sold by this shop
        ctx['new_orders'] = Order.objects.filter(
            food_list__seller__name=shop.name,
            status='paid',
        ).distinct().order_by('-time')

        ctx['accepted_orders'] = Order.objects.filter(
            food_list__seller__name=shop.name,
            status='accepted',
        ).distinct().order_by('-time')

        ctx['finished_orders'] = Order.objects.filter(
            food_list__seller__name=shop.name,
            status='finished',
        ).distinct().order_by('-time')

        return ctx
