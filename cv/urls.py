from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_cv, name='create_cv'),
]
