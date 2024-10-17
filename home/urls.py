from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('404/', views.test_404, name='404_error'),
    path('500/', views.test_500, name='500_error'),
]
