from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin_app/', admin.site.urls),
    path('', include("shop.urls", namespace="shop")),
    path('account/', include("accounts.urls", namespace="account")),
    path('dashboard/', include("dashboard.urls", namespace="dashboard"))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)