from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Department, Employee


class EmployeeAPITests(APITestCase):
    def setUp(self):
        # Create test user & department
        self.user = User.objects.create_user(username='admin', password='password123')
        self.department = Department.objects.create(
            name="Engineering", 
            description="Tech team"
        )
        # Login as authenticated user
        self.client.login(username='admin', password='password123')

    def test_department_creation(self):
        response = self.client.post('/api/departments/', {
            'name': 'HR', 
            'description': 'Human Resources'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_employee_creation_success(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "department": self.department.id,
            "salary": 75000.00
        }
        response = self.client.post('/api/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_negative_salary_rejection(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "department": self.department.id,
            "salary": -50000.00
        }
        response = self.client.post('/api/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email_rejection(self):
        Employee.objects.create(
            first_name="John", 
            last_name="Doe",
            email="duplicate@example.com", 
            department=self.department, 
            salary=50000
        )
        data = {
            "first_name": "Alice", 
            "last_name": "Smith",
            "email": "duplicate@example.com", 
            "department": self.department.id, 
            "salary": 60000
        }
        response = self.client.post('/api/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_non_existent_department_rejection(self):
        data = {
            "first_name": "Mark",
            "last_name": "Twain",
            "email": "mark@example.com",
            "department": 9999,  # Invalid ID
            "salary": 60000.00
        }
        response = self.client.post('/api/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filtering_and_search(self):
        Employee.objects.create(
            first_name="John", 
            last_name="Doe",
            email="john@example.com", 
            department=self.department, 
            salary=50000, 
            job_title="Developer"
        )
        
        # Test department filter
        filter_resp = self.client.get(f'/api/employees/?department={self.department.id}')
        self.assertEqual(filter_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(filter_resp.data), 1)

        # Test search filter
        search_resp = self.client.get('/api/employees/?search=john')
        self.assertEqual(search_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_resp.data), 1)

    def test_unauthenticated_user_permissions(self):
        self.client.logout()
        
        # GET should succeed for unauthenticated users
        get_resp = self.client.get('/api/departments/')
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)

        # POST should be rejected for unauthenticated users (DRF returns 403 Forbidden)
        post_resp = self.client.post('/api/departments/', {'name': 'Marketing'})
        self.assertIn(post_resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])