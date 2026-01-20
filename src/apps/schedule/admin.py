from django.contrib import admin
from .models import (
    Faculty, Insertion, Building, Audience, Subdivision, 
    Group, Teacher, Pair, AudiencesOfSubdivisions, 
    AudiencesOfPairs, GroupsOfPairs, TeachersOfPairs
)


class ReadOnlyModelAdmin(admin.ModelAdmin):
    """
    Base admin class for read-only models
    """
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        # Allow viewing for all users who can access admin
        return request.user.is_staff


@admin.register(Faculty)
class FacultyAdmin(ReadOnlyModelAdmin):
    list_display = ('id', 'name', 'display_name', 'short_display_name')
    search_fields = ('name', 'display_name')
    list_filter = ('name',)


@admin.register(Insertion)
class InsertionAdmin(ReadOnlyModelAdmin):
    list_display = ('id', 'date', 'faculty', 'hash')
    list_filter = ('date', 'faculty')
    search_fields = ('hash',)


@admin.register(Building)
class BuildingAdmin(ReadOnlyModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Audience)
class AudienceAdmin(ReadOnlyModelAdmin):
    list_display = ('id', 'name', 'autocreated', 'building')
    list_filter = ('autocreated', 'building')
    search_fields = ('name',)


@admin.register(Subdivision)
class SubdivisionAdmin(ReadOnlyModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Group)
class GroupAdmin(ReadOnlyModelAdmin):
    list_display = ('id', 'name', 'faculty')
    list_filter = ('faculty',)
    search_fields = ('name',)


@admin.register(Teacher)
class TeacherAdmin(ReadOnlyModelAdmin):
    list_display = ('id', 'login', 'name', 'url')
    search_fields = ('name', 'login')
    list_filter = ('login',)


@admin.register(Pair)
class PairAdmin(ReadOnlyModelAdmin):
    list_display = ('id', 'num', 'date', 'subject', 'text', 'insertion')
    list_filter = ('date', 'subject', 'insertion')
    search_fields = ('text', 'subject')
    date_hierarchy = 'date'


@admin.register(AudiencesOfSubdivisions)
class AudiencesOfSubdivisionsAdmin(ReadOnlyModelAdmin):
    list_display = ('audience', 'subdivision')
    list_filter = ('subdivision',)


@admin.register(AudiencesOfPairs)
class AudiencesOfPairsAdmin(ReadOnlyModelAdmin):
    list_display = ('audience', 'pair')
    list_filter = ('pair',)


@admin.register(GroupsOfPairs)
class GroupsOfPairsAdmin(ReadOnlyModelAdmin):
    list_display = ('group', 'pair')
    list_filter = ('pair',)


@admin.register(TeachersOfPairs)
class TeachersOfPairsAdmin(ReadOnlyModelAdmin):
    list_display = ('teacher', 'pair')
    list_filter = ('pair',)