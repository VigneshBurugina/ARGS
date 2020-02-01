from django.urls import path, include

urlpatterns = [
    path('', include('error.urls')),
    path('submit/', include('submit.urls')),
]
