from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('save_as_draft', views.save_as_draft, name='save_as_draft'),
    path('load_draft', views.load_draft, name='load_draft')
]