"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import handler404, handler500
from dashboard import views  # Ajusta según tu estructura

handler404 = views.error_404
handler500 = views.error_500


urlpatterns = [
    path("", include("dashboard.urls")),
    path('products/', include('products.urls', namespace='products')),
    path("vendors/", include("vendors.urls", namespace='vendors')),
    path("categorys/", include("categorys.urls", namespace='categorys')),
    path("customers/", include("customers.urls", namespace='customers')),
    path("stock/", include("stock.urls", namespace='stock')),
    path("pos/", include("pos.urls", namespace='pos')),
    path("reports/", include("reports.urls", namespace='reports')),
    path('admin/', admin.site.urls),
]
