from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Departments.
    - Unauthenticated users can view (GET).
    - Only authenticated users can POST, PUT, DELETE.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations, filtering, and search for Employees.
    - Unauthenticated users can view (GET).
    - Only authenticated users can POST, PUT, DELETE.
    - Supports filtering by department ID and active status.
    - Supports searching by first_name, last_name, email, and job_title.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    # Enable filtering: GET /api/employees/?department=1 & GET /api/employees/?is_active=true
    filterset_fields = ['department', 'is_active']
    
    # Enable search: GET /api/employees/?search=john
    search_fields = ['first_name', 'last_name', 'email', 'job_title']