from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_login, name='submit_login'),
]