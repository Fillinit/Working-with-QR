from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.orders, name='orders'),
    path('packaging/', views.packaging, name='packaging'),
    path('operations/', views.operations, name='operations'),
    path('marking_codes/', views.marking_codes, name='marking_codes'),
]
