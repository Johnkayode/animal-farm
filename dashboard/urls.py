from django.urls import path
from . import views


app_name = "dashboard"

urlpatterns = [
    path('', views.home, name="home"),
    path('add_product/', views.add_product, name="add_product"),
    path('edit_product/<slug:slug>/', views.edit_product, name="edit_product"),
    path('delete_product/<slug:slug>/', views.delete_product, name="delete_product"),
    path('add_category/', views.add_category, name="add_category"),
]
