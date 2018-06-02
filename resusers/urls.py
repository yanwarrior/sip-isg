from django.urls import path

from resusers import views


app_name = 'resusers'


urlpatterns = [
    path('ajax-customer-list/', views.ajax_customer_list, name="ajax_customer_list"),
]