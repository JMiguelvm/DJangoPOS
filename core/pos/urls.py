from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_vendor', views.get_vendor, name='get_vendor'),
    path('get_products', views.get_products, name='get_products'),
    path('add_stock', views.add_stock, name='add_stock')
]