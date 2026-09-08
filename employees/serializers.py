# TODO (candidate): Define DepartmentSerializer and EmployeeSerializer here
# using rest_framework.serializers.ModelSerializer, once the Department and
# Employee models exist in models.py.
#
# Remember the API must reject:
#   - duplicate employee email
#   - invalid email format
#   - negative salary
#   - a department id that doesn't exist
#
# Model-level constraints (unique=True, MinValueValidator, EmailField) are
# inherited automatically by ModelSerializer in most cases, but confirm this
# with your own tests.

from rest_framework import serializers
from .models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_at']


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'department', 'department_name', 'job_title', 'salary', 
            'date_joined', 'is_active', 'created_at'
        ]

    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value