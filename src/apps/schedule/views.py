from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import (
    Faculty, Insertion, Building, Audience, Subdivision, 
    Group, Teacher, Pair
)


class ScheduleListView(LoginRequiredMixin, ListView):
    """
    Base view for displaying schedule data
    """
    template_name = 'schedule/base.html'
    context_object_name = 'items'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Расписание'
        return context


class FacultyListView(ScheduleListView):
    model = Faculty
    template_name = 'schedule/faculty_list.html'


class TeacherListView(ScheduleListView):
    model = Teacher
    template_name = 'schedule/teacher_list.html'


class GroupListView(ScheduleListView):
    model = Group
    template_name = 'schedule/group_list.html'


class PairListView(ScheduleListView):
    model = Pair
    template_name = 'schedule/pair_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Optionally filter by date or other criteria
        return queryset.select_related('insertion').prefetch_related('groups', 'teachers', 'audiences')


class BuildingListView(ScheduleListView):
    model = Building
    template_name = 'schedule/building_list.html'


class AudienceListView(ScheduleListView):
    model = Audience
    template_name = 'schedule/audience_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('building')