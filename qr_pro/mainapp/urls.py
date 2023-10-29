from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.log_in, name='log_in'),
    path('main/', views.index, name='index'),

    path('orders/', views.orders, name='orders'),
    path('orders/<int:orders_id>/', views.orders_more, name='orders_more'),
    path('orders/add', views.orders_add, name='orders_add'),
    path('orders/save', views.orders_save, name='orders_save'),

    path('packaging/', views.packaging, name='packaging'),
    path('packaging/<int:pack_id>/', views.pack_more, name='pack_more'),
    path('packaging/api/scan/', views.scan_pack, name='scan_pack'),
    path('pro/packaging/api/scan/', views.scan_pro_pack, name='scan_prod_pack'),

    path('operations/', views.operations, name='operations'),
    path('operations/<int:operation_id>/', views.operations_more, name='operations_more'),
    path('operations/api/scan/', views.scanOperMC, name='scan_oper'),

    path('marking_codes/', views.marking_codes, name='marking_codes'),
    path('marking_codes/api/scan/', views.scanMarkCodes, name='scan_pack'),

    path('print_pdf/', views.print_pdf, name='print_pdf'),
    path('open_pdf/', views.open_pdf, name='open_pdf'),


    path('del_marking/', views.del_marking, name='del_marking'),

]
