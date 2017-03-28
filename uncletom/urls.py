from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^shop-manager/', include('shop_manager.urls', namespace='shop_manager')),
    url(r'', include('market.urls', namespace='market')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
