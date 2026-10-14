from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='regsiter'),
    path('login/', views.login_user, name='login'),
    path('auth/', views.user_list_create, name='user_list_create'),
]