from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('resproducts/', include('resproducts.urls')),
    path('resusers/', include('resusers.urls')),
    path('resorders/', include('resorders.urls')),
]
