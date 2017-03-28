from django.conf.urls import url

from . import views


urlpatterns = [
    # the index page, showing all the shops
    url(r'^$', views.ShopManageView.as_view(), name='shop-manage'),

    # the page for opening a new shop
    url(r'^new-food/$', views.NewFoodView.as_view(), name='new-food'),
]
