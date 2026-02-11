from django.urls import path,include

from . import views


urlpatterns = [

    path('auth/', views.user_list_create, name= 'user_list_create')

]