from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_vendor', views.get_vendor, name='get_vendor'),
    path('get_products', views.get_products, name='get_products'),
    path('get_product_by_barcode', views.get_product_by_barcode, name='get_product_by_barcode'),
    path('get_stock', views.get_stock, name='get_stock'),
    path('add_stock', views.add_stock, name='add_stock'),
    path('get_orders', views.get_orders, name='get_orders'),
    path('get_specific_order', views.get_specific_order, name='get_specific_order'),
    path('make_order', views.make_order, name='make_order')
]