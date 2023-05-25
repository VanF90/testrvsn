from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('transfer/', include('transactions.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]
