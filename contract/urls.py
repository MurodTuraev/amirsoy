from django.urls import path
from .views import *

urlpatterns = [
    path('', contract_create, name='contract_create'),
    path('contract_list/', contract_list, name='contract_list'),
    path('contract_detail/<slug:slug>/', contract_detail, name='contract_detail'),
    path('contract_payment/<slug:slug>/', contract_payment, name='contract_payment'),
]