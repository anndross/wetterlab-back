from django.contrib import admin
from django.urls import path
from .views import LoginView, TestView, DecodeTokenView, AvailableServices

urlpatterns = [
    path('login', LoginView.as_view()),
    path('decode-token', DecodeTokenView.as_view()),
    path('test', TestView.as_view()),
    path('available-services', AvailableServices.as_view())
]
