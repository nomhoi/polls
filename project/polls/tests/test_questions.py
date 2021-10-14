from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class QuestionsByAdminAPITestCase(APITestCase):
    fixtures = ['users', 'polls']

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.client.force_login(self.user)

    def test_list(self):
        resp = self.client.get('/api/v1/questions/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = '/api/v1/questions/'
        data = {
            "text": "Новый вопрос",
            "type": 2,
            "pool": 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        url = '/api/v1/questions/2/'
        data = {
            "text": "Обновление вопроса",
            "type": 2,
            "pool": 2
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        url = '/api/v1/questions/2/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class QuestionsByUserAPITestCase(APITestCase):
    fixtures = ['users', 'polls']

    def setUp(self):
        self.user = User.objects.get(username='user')
        self.client.force_login(self.user)

    def test_list(self):
        resp = self.client.get('/api/v1/questions/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = '/api/v1/questions/'
        data = {
            "text": "Новый вопрос",
            "type": 2,
            "pool": 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        url = '/api/v1/questions/2/'
        data = {
            "text": "Обновление вопроса",
            "type": 2,
            "pool": 2
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy(self):
        url = '/api/v1/questions/2/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
