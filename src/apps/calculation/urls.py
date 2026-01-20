from django.urls import path
from . import views

urlpatterns = [
    path('', views.PairSearchView.as_view(), name='pair-search'),
]