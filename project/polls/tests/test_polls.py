from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class PollsByAdminAPITestCase(APITestCase):
    fixtures = ['users', 'polls']

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.client.force_login(self.user)

    def test_list(self):
        response = self.client.get('/api/v1/polls/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = '/api/v1/polls/'
        data = {
            "name": "Новый опрос",
            "start_date": "2021-10-13T02:09:43Z",
            "end_date": "2021-10-27T02:09:51Z",
            "description": "Описание нового опроса"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        url = '/api/v1/polls/2/'
        data = {
            "name": "Обновление опроса",
            "start_date": "2021-10-13T02:09:43Z",
            "end_date": "2021-10-27T02:09:51Z",
            "description": "Обновление опроса"
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        url = '/api/v1/polls/2/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PollsByUserAPITestCase(APITestCase):
    fixtures = ['users', 'polls']

    def setUp(self):
        self.user = User.objects.get(username='user')
        self.client.force_login(self.user)

    def test_list(self):
        response = self.client.get('/api/v1/polls/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = '/api/v1/polls/'
        data = {
            "name": "Новый опрос",
            "start_date": "2021-10-13T02:09:43Z",
            "end_date": "2021-10-27T02:09:51Z",
            "description": "Описание нового опроса"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        url = '/api/v1/polls/2/'
        data = {
            "name": "Обновление опроса",
            "start_date": "2021-10-13T02:09:43Z",
            "end_date": "2021-10-27T02:09:51Z",
            "description": "Обновление опроса"
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy(self):
        url = '/api/v1/polls/2/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
