from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from general.views import Custom500ErrorView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include([
        path('accounts/', include('account.urls')),
        path('trips/', include('trip.urls')),
        path('orders/', include('order.order_urls')),
        path('payments/', include('order.payment_urls')),
        path('reviews/', include('order.review_urls')),
    ])),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

handler500 = Custom500ErrorView.as_view()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)