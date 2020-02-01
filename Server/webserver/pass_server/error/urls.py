from django.urls import path
from error import views

urlpatterns = [
    path('', views.index, name='error'),
]
