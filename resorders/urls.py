from django.urls import path

from resorders import views


app_name = 'resorders'


urlpatterns = [
    path('order/add/', views.order_add, name="order_add"),
    # path('order/list/', views.order_list, name='order_list'),
    path('ajax/order/add/', views.ajax_order_add, name="ajax_order_add"),
]