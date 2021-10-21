# Тестовое задание

Задача: спроектировать и разработать API для системы опросов пользователей.

Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API


# Инструкция по разворачиванию приложения локально


```bash
git clone git@github.com:nomhoi/polls.git
cd polls

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py runserver
```


# Endpoints


## Get User ID

```
GET /api/v1/main/
```

Клиентское приложение при первом обращении к бэкенду анонимного пользователя выполняет этот запрос с заголовком HTTP_X_USERID без указания ID, регистрирует его в базе и возвращает User ID пользователю, который сохраняется в клиентском приложении.

Не требует аутентификации.

Примечение: не реализовано в коде.


## Authentication Header

Все запросы описанные ниже для анонимных пользователей выполняются с включением заголовка HTTP_X_USERID с указанием ID пользователя. Аутентификация выполняется с помощью бэкенда аутентификации UserIdAuthentication.

В запросах администраторов и зарегистрированных пользователях этот заголовок отсутствует. Аутентификация выполняется с помощью выбранного бэкенда аутентификации (не реализовано в коде).


## List Polls

```
GET /api/v1/polls/
```

Возвращает список опросов. Требуется аутентификация.


## Get Poll

```
GET /api/v1/polls/:id/
```

Возвращает опрос. Требуется аутентификация.


## Create Poll

```
POST /api/v1/polls/
```

Пример тела запроса:
```
{
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
                    "text": "Respond variant 1"
                },
                {
                    "text": "Respond variant 2"
                }
            ]
        },
        {
            "type": 3,
            "text": "Question 3",
            "choices": [
                {
                    "text": "Respond variant 1"
                },
                {
                    "text": "Respond variant 2"
                }
            ]
        }
    ]
}
```

Создает и возвращает новый опрос.

Требуется аутентификация, разрешено только админу.


## Update Poll for Admins

```
PUT /api/v1/polls/:id/
```

Пример тела запроса для админа:
```
{
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
                    "text": "Respond variant 1"
                },
                {
                    "text": "Respond variant 2"
                }
            ]
        },
        {
            "type": 3,
            "text": "Question 3",
            "choices": [
                {
                    "text": "Respond variant 1"
                },
                {
                    "text": "Respond variant 2"
                }
            ]
        }
    ]
}
```

Обновляет и возвращает новый опрос.

Требуется аутентификация, разрешено только админу.


## Update Poll for Users

```
PUT /api/v1/responses/:id/
```

Пример тела запроса для пользователя:
```
{
    "id": 1,
    "responses": [
        {
            "id": 1,
            "boolean_response": null,
            "text_response": "My response.",
            "user": 2,
            "poll": 1,
            "choice": 15
        },
        {
            "id": 2,
            "boolean_response": true,
            "text_response": "",
            "user": 2,
            "poll": 1,
            "choice": 4
        },
        {
            "id": 3,
            "boolean_response": true,
            "text_response": "",
            "user": 2,
            "poll": 1,
            "choice": 6
        },
        {
            "id": 4,
            "boolean_response": true,
            "text_response": "",
            "user": 2,
            "poll": 1,
            "choice": 7
        }
    ]
}
```

Обновляет модель UserResponse. Возвращает обновленный опрос.
В список responses включать только те ответы, которые были изменены в клиентском приложении.

Требуется аутентификация.


## Delete Poll

```
DELETE /api/v1/polls/:id/
```

Удаляет опрос.

Требуется аутентификация, разрешено только админу.


# API Response format


## Single Poll for Admin

```
    "id": 1,
    "name": "Poll 1",
    "start_date": "2021-10-13T02:09:43Z",
    "end_date": "2021-10-27T02:09:51Z",
    "description": "Poll 1 description",
    "questions": [
        {
            "id": 1,
            "type": 1,
            "text": "Question 1",
            "choices": [
                {
                    "id": 15,
                    "choice": null
                }
            ]
        },
        {
            "id": 2,
            "type": 2,
            "text": "Question 2",
            "choices": [
                {
                    "id": 4,
                    "choice": "Respond 1"
                },
                {
                    "id": 5,
                    "choice": "Respond 2"
                }
            ]
        },
        {
            "id": 3,
            "type": 3,
            "text": "Question 3",
            "choices": [
                {
                    "id": 6,
                    "choice": "Respond 1"
                },
                {
                    "id": 7,
                    "choice": "Respond 2"
                },
                {
                    "id": 14,
                    "choice": "Respond 3"
                }
            ]
        },
        {
            "id": 4,
            "type": 1,
            "text": "Question 4",
            "choices": [
                {
                    "id": 16,
                    "choice": null
                }
            ]
        }
    ]
}
```


## Single Poll for Users

Ответ после запроса GET /api/v1/polls/:id/

```
{
    "id": 1,
    "name": "Poll 1",
    "start_date": "2021-10-13T02:09:43Z",
    "end_date": "2021-10-27T02:09:51Z",
    "description": "Poll 1 description",
    "questions": [
        {
            "id": 1,
            "type": 1,
            "text": "Question 1",
            "choices": [
                {
                    "id": 15,
                    "choice": null,
                    "respond_id": 1,
                    "respond": "My response."
                }
            ]
        },
        {
            "id": 2,
            "type": 2,
            "text": "Question 2",
            "choices": [
                {
                    "id": 4,
                    "choice": "Respond 1",
                    "respond_id": 2,
                    "respond": true
                },
                {
                    "id": 5,
                    "choice": "Respond 2",
                    "respond": false
                }
            ]
        },
        {
            "id": 3,
            "type": 3,
            "text": "Question 3",
            "choices": [
                {
                    "id": 6,
                    "choice": "Respond 1",
                    "respond_id": 3,
                    "respond": true
                },
                {
                    "id": 7,
                    "choice": "Respond 2",
                    "respond_id": 4,
                    "respond": true
                },
                {
                    "id": 14,
                    "choice": "Respond 3",
                    "respond": false
                }
            ]
        },
        {
            "id": 4,
            "type": 1,
            "text": "Question 4",
            "choices": [
                {
                    "id": 16,
                    "choice": null,
                    "respond": ""
                }
            ]
        }
    ]
}
```


## Single Poll for Users

Ответ после запроса PUT /api/v1/responses/:id/ 

```
{
    "id": 1,
    "responses": [
        {
            "id": 1,
            "boolean_response": null,
            "text_response": "My response.",
            "user": 2,
            "poll": 1,
            "choice": 15
        },
        {
            "id": 2,
            "boolean_response": true,
            "text_response": "",
            "user": 2,
            "poll": 1,
            "choice": 4
        },
        {
            "id": 3,
            "boolean_response": true,
            "text_response": "",
            "user": 2,
            "poll": 1,
            "choice": 6
        },
        {
            "id": 4,
            "boolean_response": true,
            "text_response": "",
            "user": 2,
            "poll": 1,
            "choice": 7
        }
    ]
}
```


## Multiple Polls

```
[
    {
        "id": 1,
        "name": "Poll 1",
        "start_date": "2021-10-13T02:09:43Z",
        "end_date": "2021-10-27T02:09:51Z",
        "description": "Poll 1 description"
    },
    {
        "id": 2,
        "name": "Poll 2",
        "start_date": "2021-10-13T05:33:53Z",
        "end_date": "2021-10-28T05:33:57Z",
        "description": "Poll 2 description"
    }
]
```
