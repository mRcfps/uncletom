from django.views.generic import CreateView, TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import NewFoodForm


class ShopManageView(TemplateView):
    template_name = 'shop_manager/shop_manage.html'

    def get_context_data(self, **kwargs):
        ctx = super(ShopManageView, self).get_context_data(**kwargs)
        ctx['shop'] = self.request.user.shop.get()
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
