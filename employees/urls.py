from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, EmployeeViewSet

# DRF DefaultRouter automatically generates all standard RESTful routes:
# GET /api/departments/, POST /api/departments/, GET/PUT/DELETE /api/departments/<id>/
# GET /api/employees/, POST /api/employees/, GET/PUT/DELETE /api/employees/<id>/
router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]