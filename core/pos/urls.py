from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_vendor', views.get_vendor, name='get_vendor'),
    path('get_products', views.get_products, name='get_products'),
    path('get_product_by_barcode', views.get_product_by_barcode, name='get_product_by_barcode'),
    path('get_stock', views.get_stock, name='get_stock'),
    path('add_stock', views.add_stock, name='add_stock')
]