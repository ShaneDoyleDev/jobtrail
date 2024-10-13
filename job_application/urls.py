from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_application_list, name='job_application_list'),
    path('new/', views.job_application_create, name='job_application_create'),
    path('<int:pk>/edit/', views.job_application_update, name='job_application_update'),
    path('<int:pk>/delete/', views.job_application_delete, name='job_application_delete'),
]