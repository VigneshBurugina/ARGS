from django.urls import path
from submit import views

urlpatterns = [
    path('', views.index, name='submit'),
]
