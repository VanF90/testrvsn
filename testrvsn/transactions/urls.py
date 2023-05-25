from django.urls import path
from .views import TransferView

urlpatterns = [
    path('', TransferView.as_view(), name='transfer'),
]