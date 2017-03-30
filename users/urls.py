from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/users/login'}, name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
