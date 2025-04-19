import json
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User

class TestUserView(APITestCase):
    def setUp(self):
        user = User(name='Test1', dni='09876543210')
        user.save()
        self.url = reverse("users-list")
        self.data = {'name': 'Test2', 'dni': '09876543211'}

    def test_post(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content), {"id": 2, "name":"Test2", "dni":"09876543211"})
        self.assertEqual(User.objects.count(), 2)

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_get(self):
        response = self.client.get(self.url + '1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"id": 1, "name":"Test1", "dni":"09876543210"})

    def test_post_duplicate_user(self):
        duplicate_data = {'name': 'TestX', 'dni': '09876543210'}
        response = self.client.post(self.url, duplicate_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], 'User already exists')
        self.assertEqual(User.objects.count(), 1)

    def test_post_invalid_data(self):
        response = self.client.post(self.url, {'name': 'Test3'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('dni', response.data)

    def test_delete_user_not_allowed(self):
        response = self.client.delete(self.url + '1/')
        self.assertEqual(response.status_code, 405)

    def test_get_nonexistent_user(self):
        response = self.client.get(self.url + '999/')
        self.assertEqual(response.status_code, 404)

    def test_patch_user(self):
        patch_data = {'name': 'Updated Name'}
        response = self.client.patch(self.url + '1/', patch_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Name')
