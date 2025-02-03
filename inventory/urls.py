from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # Product section
    path('product', views.productList, name='productList'),
    path('product/add', views.addProduct, name='addProduct'),
    path('product/edit', views.editProduct, name='editProduct'),
    path('product/delete', views.deleteProduct, name='deleteProduct'),
    path('product/search', views.searchProduct, name='searchProduct'),
    # Vendor section
    path('vendor', views.vendorList, name='vendorList'),
    path('vendor/add', views.addVendor, name='addVendor'),
    path('vendor/edit', views.editVendor, name='editVendor'),
    path('vendor/delete', views.deleteVendor, name='deleteVendor'),
    path('vendor/search', views.searchVendor, name='searchVendor'),
    # Category section
    path('category', views.categoryList, name='categoryList'),
    path('category/add', views.addCategory, name='addCategory'),
    path('category/edit', views.editCategory, name='editCategory'),
    path('category/delete', views.deleteCategory, name='deleteCategory'),
    path('category/search', views.searchCategory, name='searchCategory'),
    # Customer section
    path('customer', views.customerList, name='customerList'),
    path('customer/add', views.addCustomer, name='addCustomer'),
    path('customer/edit', views.editCustomer, name='editCustomer'),
    path('customer/delete', views.deleteCustomer, name='deleteCustomer'),
    path('customer/search', views.searchCustomer, name='searchCustomer'),
    # Customer section
    path('debt', views.debtView, name='debtView'),
    path('debt/add', views.addDebt, name='addDebt'),
    path('debt/delete', views.deleteDebt, name='deleteDebt'),
    # POS
    path('pos', views.posView, name='posView'),
    path('order', views.orderView, name='orderView'),
    # Stock
    path('stock', views.productStockList, name='productStockList'),
    path('stock/add', views.addStock, name='addStock'),
    path('stock/item', views.productStock, name='productStock'),
    path('test', views.createData, name='test'),
]

# urlpatterns = [
#     path('productList', views.productList, name='productList'),
#     path('addProduct/', views.addProduct),
#     path('editProduct', views.editProduct, name='editProduct'),
#     path('deleteProduct', views.deleteProduct, name='deleteProduct'),
#     path('searchProduct', views.searchProduct, name='searchProduct'),
#     # Vendor section
#     path('vendorList', views.vendorList, name='vendorList'),
#     path('addVendor', views.addVendor, name='addVendor'),
#     path('editVendor', views.editVendor, name='editVendor'),
#     path('deleteVendor', views.deleteVendor, name='deleteVendor'),
#     path('searchVendor', views.searchVendor, name='searchVendor'),
#     # Category section
#     path('categoryList', views.categoryList, name='categoryList'),
#     path('addCategory', views.addCategory, name='addCategory'),
#     path('editCategory', views.editCategory, name='editCategory'),
#     path('deleteCategory', views.deleteCategory, name='deleteCategory'),
#     path('searchCategory', views.searchCategory, name='searchCategory'),
#     # Customer section
#     path('customerList', views.customerList, name='customerList'),
#     path('addCustomer', views.addCustomer, name='addCustomer'),
#     path('editCustomer', views.editCustomer, name='editCustomer'),
#     path('deleteCustomer', views.deleteCustomer, name='deleteCustomer'),
#     path('searchCustomer', views.searchCustomer, name='searchCustomer'),
#     # Customer section
#     path('debtView', views.debtView, name='debtView'),
#     path('addDebt', views.addDebt, name='addDebt'),
#     path('deleteDebt', views.deleteDebt, name='deleteDebt'),
#     # POS
#     path('posView', views.posView, name='posView'),
#     path('orderView', views.orderView, name='orderView'),
#     # Stock
#     path('stockList/', views.productStockList, name='productStockList'),
#     path('addStock/', views.addProductStock, name='addProductStock'),
#     path('itemStock/', views.itemStock, name='itemStock'),
# ]