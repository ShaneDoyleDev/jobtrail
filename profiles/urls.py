from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.profile_update, name='profile_update'),
]
