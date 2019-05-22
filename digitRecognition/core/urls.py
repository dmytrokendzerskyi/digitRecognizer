from django.urls import path, reverse
from . import views, rest

urlpatterns = [
    path('', views.index, name = 'index'),
    path('image', rest.recognizeImage, name = 'recognizeImage')
]