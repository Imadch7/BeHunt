from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit_signup/', views.submit_signup, name='submit_login'),
]