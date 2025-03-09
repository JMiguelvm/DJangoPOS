from django.urls import path
from . import views


app_name = 'categorys'

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/', views.edit, name='edit'),
    path('create/', views.create, name='create')
]