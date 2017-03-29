from django.conf.urls import url

from . import views

urlpatterns = [
    # the index page, showing all the shops
    url(r'^$', views.ShopManageView.as_view(), name='shop-manage'),

    # the page for opening a new shop
    url(r'^new-food/$', views.NewFoodView.as_view(), name='new-food'),

    # the page for displaying and managing orders
    url(
        r'^order-management/$',
        views.OrderManagementView.as_view(),
        name='order-management',
    ),

    # a simple view to handle user's accepting orders logic
    url(
        r'^accept-order/(?P<order_id>\d+)/$',
        views.AcceptOrderView.as_view(),
        name='accept-order',
    ),
]
