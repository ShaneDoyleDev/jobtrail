from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test-404/', views.test_404, name='404_error'),
]
