import json
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

    def test_get(self):
        response = self.client.get('/api/v1/polls/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(response.data['name'], 'Poll 1')
        self.assertEqual(len(response.data['questions']), 4)
                
    def test_create(self):
        url = '/api/v1/polls/'
        data = {
            "name": "New poll",
            "start_date": "2021-10-13T02:09:43Z",
            "end_date": "2021-10-27T02:09:51Z",
            "description": "New poll description",          
            "questions": [
                {
                    "type": 1,
                    "text": "Question 1",
                    "choices": []
                },
                {
                    "type": 2,
                    "text": "Question 2",
                    "choices": [
                        {
                            "choice": "Respond variant 1"
                        },
                        {
                            "choice": "Respond variant 2"
                        }
                    ]
                },
                {
                    "type": 3,
                    "text": "Question 3",
                    "choices": [
                        {
                            "choice": "Respond variant 1"
                        },
                        {
                            "choice": "Respond variant 2"
                        }
                    ]
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        url = '/api/v1/polls/2/'
        data = {
            "name": "Change poll",
            "start_date": "2021-10-13T02:09:43Z",
            "end_date": "2021-10-27T02:09:51Z",
            "description": "Change poll description",
            "questions": [
                {
                    "type": 1,
                    "text": "Question 1",
                    "choices": []
                },
                {
                    "type": 2,
                    "text": "Question 2",
                    "choices": [
                        {
                            "choice": "Respond variant 1"
                        },
                        {
                            "choice": "Respond variant 2"
                        }
                    ]
                },
                {
                    "type": 3,
                    "text": "Question 3",
                    "choices": [
                        {
                            "choice": "Respond variant 1"
                        },
                        {
                            "choice": "Respond variant 2"
                        }
                    ]
                }
            ]
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

    def test_get_poll_1(self):
        response = self.client.get('/api/v1/polls/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(response.data['name'], 'Poll 1')
        self.assertEqual(len(response.data['questions']), 4)

    def test_get_poll_2(self):
        response = self.client.get('/api/v1/polls/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(response.data['name'], 'Poll 2')
        self.assertEqual(len(response.data['questions']), 3)

    def test_create(self):
        url = '/api/v1/polls/'
        data = {
            "questions": [
                {
                    "type": 1,
                    "text": "Question 1",
                    "choices": []
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        url = '/api/v1/polls/2/'
        data = {
            "name": "Change poll",
            "start_date": "2021-10-13T02:09:43Z",
            "end_date": "2021-10-27T02:09:51Z",
            "description": "Change poll description",
            "questions": [
                {
                    "type": 1,
                    "text": "Question 1",
                    "choices": []
                },
                {
                    "type": 2,
                    "text": "Question 2",
                    "choices": [
                        {
                            "choice": "Respond variant 1"
                        },
                        {
                            "choice": "Respond variant 2"
                        }
                    ]
                },
                {
                    "type": 3,
                    "text": "Question 3",
                    "choices": [
                        {
                            "choice": "Respond variant 1"
                        },
                        {
                            "choice": "Respond variant 2"
                        }
                    ]
                }
            ]
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy(self):
        url = '/api/v1/polls/2/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserResponseAPITestCase(APITestCase):
    fixtures = ['users', 'polls']

    def setUp(self):
        self.user = User.objects.get(username='user')
        self.client.force_login(self.user)

    def test_list(self):
        response = self.client.get('/api/v1/responses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self):
        response = self.client.get('/api/v1/responses/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
       
    def test_update(self):
        url = '/api/v1/responses/2/'

        # Если ответ отсутствует в модели UserResponse, то не нужно указывать id.
        # Ответ будет добавлен в модель UserResponse с новым id.
        data = {
            "id": 2,
            "responses": [
                {                    
                    "boolean_response": None,
                    "text_response": "My response.",
                    "user": 2,
                    "poll": 2,
                    "choice": 17
                }            
            ]
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_id = response.data['responses'][0]['id']

        # Для обновления ответа нужно указать id ответа.
        data = {
            "id": 2,
            "responses": [
                {
                    "id": response_id,
                    "boolean_response": None,
                    "text_response": "Response changed.",
                    "user": 2,
                    "poll": 2,
                    "choice": 17
                }            
            ]
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Если происходит попытка изменить ответ с неправильным id ответа с существующим id варианта 
        # ответа (choice), то поднимется исключение - id варианта ответа должен быть уникальным.
        data = {
            "id": 2,
            "responses": [
                {
                    "id": response_id + 1,
                    "boolean_response": None,
                    "text_response": "My response.",
                    "user": 2,
                    "poll": 2,
                    "choice": 17
                }            
            ]
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
