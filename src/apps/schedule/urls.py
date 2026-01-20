from django.urls import path
from . import views

urlpatterns = [
    path('', views.PairListView.as_view(), name='schedule-home'),
    path('faculties/', views.FacultyListView.as_view(), name='faculties-list'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers-list'),
    path('groups/', views.GroupListView.as_view(), name='groups-list'),
    path('pairs/', views.PairListView.as_view(), name='pairs-list'),
    path('buildings/', views.BuildingListView.as_view(), name='buildings-list'),
    path('audiences/', views.AudienceListView.as_view(), name='audiences-list'),
]