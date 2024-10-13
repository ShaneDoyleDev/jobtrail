from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_job_application, name='create'),
    path('detailed/<int:id>/', views.detailed__job_application, name='detailed__job_application'),
    path('download/<str:doc_type>/<int:application_id>/', views.download_doc, name='download_doc'),
]
