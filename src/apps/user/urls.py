from django.urls import path
from .views import (
    HomeView,
    CustomLoginView,
    RegisterView,
    CustomLogoutView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]