from django.urls import path
from . import views

urlpatterns = [
    path('transfer_money/', views.transfer_money, name='transfer_money'),
]