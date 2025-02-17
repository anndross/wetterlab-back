from django.urls import path
from .views import LoginView, AvailableServices

urlpatterns = [
    path('login', LoginView.as_view()),
    path('available-services', AvailableServices.as_view())
]
