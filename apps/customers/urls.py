from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),

    path('create/', views.customer_create, name='customer_create'),

    path('edit/<int:customer_id>/', views.customer_update, name='customer_update'),

    path('deactivate/<int:customer_id>/', views.customer_deactivate, name='customer_deactivate'),
]