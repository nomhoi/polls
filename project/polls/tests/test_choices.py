from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

# TODO: remove

class ChoicesByAdminAPITestCase(APITestCase):
    fixtures = ['users', 'polls']

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.client.force_login(self.user)

    def test_list(self):
        response = self.client.get('/api/v1/choices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = '/api/v1/choices/'
        data = {
            "text": "ответ 1",
            "question": 2
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        url = '/api/v1/choices/4/'
        data = {
            "text": "ответ 11",
            "question": 2
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        url = '/api/v1/choices/4/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ChoicesByUserAPITestCase(APITestCase):
    fixtures = ['users', 'polls']

    def setUp(self):
        self.user = User.objects.get(username='user')
        self.client.force_login(self.user)

    def test_list(self):
        response = self.client.get('/api/v1/choices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = '/api/v1/choices/'
        data = {
            "text": "ответ 1",
            "question": 2
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        url = '/api/v1/choices/4/'
        data = {
            "text": "ответ 11",
            "question": 2
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy(self):
        url = '/api/v1/choices/4/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
