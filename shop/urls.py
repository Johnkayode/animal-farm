from django.urls import path
from . import views


app_name = "shop"

urlpatterns = [
    path('', views.home, name="home"),
    path('enquire/', views.enquire, name="enquire"),
    path('shop/', views.shop, name="shop"),
    path('shop/product/<slug:product_slug>/', views.product_detail, name="product_detail"),
    path('shop/<slug:category_slug>/', views.shop, name="shop_by_category"),
]