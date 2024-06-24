from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from general.views import Custom500ErrorView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include([
        path('accounts/', include('account.urls')),
        path('trips/', include('trip.urls')),
    ])),
]

handler500 = Custom500ErrorView.as_view()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
