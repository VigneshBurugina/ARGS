from django.urls import path, include

urlpatterns = [
    path('', include('error.urls')),
    path('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/', include('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.urls')),
    path('submit/', include('submit.urls')),
]
