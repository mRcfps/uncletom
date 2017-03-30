from django.shortcuts import render
from django.views.generic import \
    View, TemplateView, ListView, CreateView, DetailView
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Shop, Food, Order, Comment
from .forms import NewShopForm
from common import orderoperators


class HomeView(ListView):
    template_name = 'market/home.html'
    context_object_name = 'shops'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.user

        # check out whether the user has logged in and has a shop
        try:
            if user.is_authenticated and user.shop:
                ctx['has_shop'] = True
            else:
                ctx['has_shop'] = False
        except:
            # Handle RelatedObjectDoesNotExist error
            ctx['has_shop'] = False

        return ctx

    def get_queryset(self):
        return Shop.objects.exclude(owner=self.request.user)


class NewShopView(CreateView):
    template_name = 'market/new_shop.html'
    model = Shop
    fields = ['name', 'logo']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewShopView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        new_shop = form.save(commit=False)
        new_shop.owner = self.request.user
        new_shop.save()

        return HttpResponseRedirect(reverse('shop_manager:shop-manage'))


class ShopDetailView(ListView):
    template_name = 'market/shop.html'
    context_object_name = 'foods'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ShopDetailView, self).dispatch(*args, **kwargs)

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
    # Only POST method will be handled in Checkout View
    http_method_names = ('post', )

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CheckoutView, self).dispatch(*args, **kwargs)

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
    # Only POST method will be handled in Pay View
    http_method_names = ('post', )

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PayView, self).dispatch(*args, **kwargs)

    def post(self, request):
        orderoperators.create_order(request)
        return render(request, 'market/pay_success.html')


class MyOrdersView(TemplateView):
    template_name = 'market/my_orders.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyOrdersView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(MyOrdersView, self).get_context_data(**kwargs)

        ctx['paid_orders'], ctx['accepted_orders'], ctx['finished_orders'] = \
            orderoperators.fetch_orders_for_customer(self.request)

        return ctx


class FinishOrderView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs['order_id'])
        if order.customer != self.request.user:
            # This order does not belong to the current user in which
            # case we will block his/her request
            raise Http404
        else:
            return super(FinishOrderView, self).dispatch(*args, **kwargs)

    def get(self, request, order_id):
        orderoperators.finish_order(request, order_id)
        context = {'order': Order.objects.get(id=order_id)}

        return render(request, 'market/comment.html', context)


class CommentView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs['order_id'])
        if order.customer != self.request.user:
            # This order does not belong to the current user in which
            # case we will block his/her request
            raise Http404
        else:
            return super(CommentView, self).dispatch(*args, **kwargs)

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
