from django.conf.urls import url

from . import views

urlpatterns = [
    # the index page, showing all the shops
    url(r'^$', views.ShopManageView.as_view(), name='shop-manage'),

    # the page for adding new food
    url(r'^new-food/$', views.NewFoodView.as_view(), name='new-food'),

    # the page for update food information
    url(
        r'^update-food/(?P<pk>\d+)/$',
        views.UpdateFoodView.as_view(),
        name='update-food',
    ),

    # handle deleting food
    url(
        r'^delete-food/(?P<pk>\d+)/$',
        views.DeleteFoodView.as_view(),
        name='delete-food',
    ),

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
