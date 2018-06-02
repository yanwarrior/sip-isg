from django.urls import path

from resproducts import views


app_name = 'resproducts'


urlpatterns = [
    path('ajax-category-list/', views.ajax_category_list, name="ajax_category_list"),
    path('ajax-product-list/', views.ajax_product_list, name="ajax_product_list"),
]