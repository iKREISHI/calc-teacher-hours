from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'middle_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'middle_name')
    ordering = ('username',)

    # Define fieldsets to include middle_name
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('middle_name',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('middle_name',)}),
    )
