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
# Serve media files in development and production (temporary solution)
# For production, consider using cloud storage like Cloudinary or AWS S3n
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)