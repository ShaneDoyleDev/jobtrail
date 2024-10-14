from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.JobApplicationListView.as_view(), name='dashboard'),
    path('<int:pk>/', views.JobApplicationDetailView.as_view(), name='jobapplication_detail'),
    path('create/', views.JobApplicationCreateView.as_view(), name='jobapplication_create'),
    path('update/<int:pk>/', views.JobApplicationUpdateView.as_view(), name='jobapplication_update'),
    path('download/<str:doc_type>/<int:application_id>/', views.download_doc, name='download_doc'),
]
