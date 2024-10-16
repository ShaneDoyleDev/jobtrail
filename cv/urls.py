from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_cv, name='create_cv'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
]
