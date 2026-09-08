from django.contrib import admin
from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'email', 
        'department', 'job_title', 'salary', 'is_active'
    )
    list_filter = ('department', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'job_title')