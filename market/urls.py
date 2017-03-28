from django.conf.urls import url

from . import views

urlpatterns = [
    # the index page, showing all the shops
    url(r'^$', views.HomeView.as_view(), name='home'),

    # the page for opening a new shop
    url(r'^new-shop/$', views.NewShopView.as_view(), name='new-shop'),

    # a detailed page of a shop with a list of food
    url(
        r'^shop/(?P<shop_id>\d+)/$',
        views.ShopDetailView.as_view(),
        name='shop'
    ),

    # a detailed page of the food
    url(
        r'^shop/(?P<shop_id>\d+)/food/(?P<pk>\d+)/$',
        views.FoodDetailView.as_view(),
        name='food-detail'
    ),

    # my orders page
    url(
        r'^my-orders/$',
        views.MyOrdersView.as_view(),
        name='my-orders',
    ),

    # checkout page(POST method only)
    url(r'^checkout/$', views.CheckoutView.as_view(), name='checkout'),

    # handle paying logic and redirects to pay_success page
    url(r'^pay/$', views.PayView.as_view(), name='pay'),
]
