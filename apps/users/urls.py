
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='crm_user_list'),
    path('create/', views.user_create, name='crm_user_create'),
    path('<int:user_id>/toggle-active/', views.user_toggle_active, name='crm_user_toggle_active'),
]
