from django.contrib import admin
from django.urls import include, include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('job-application/', include('job_application.urls')),
    path('profile/', include('profiles.urls')),
    path('accounts/', include('allauth.urls')),
    path('test/', include('home.urls')),
    path('', include('home.urls')),
    path('cv/', include('cv.urls')),
]
urlpatterns += static(settings.STATIC_URL, documents_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, documents_root=settings.MEDIA_ROOT)