from django.views.generic import View, ListView, CreateView, DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Shop, Food
from .forms import NewShopForm


class HomeView(ListView):
    template_name = 'market/home.html'
    model = Shop
    context_object_name = 'shops'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)

        # check out whether the user has a shop
        ctx['has_shop'] = True if self.request.user.shop.all() else False

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
    template_name = 'market/checkout.html'

    def post(self, request):
        pass
