from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('catalog/', include('catalog.urls')),
    path('orders/', include('orders.urls')),
    path('cart/', include('cart.urls')),
    path('account/', include('accounts.urls')),
    path('feedback/', include('feedback.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)