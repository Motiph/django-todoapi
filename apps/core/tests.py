import json

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from .models import Todo


class TodoTestCase(TestCase):
    def setUp(self):
        # se crear un usuario para tener un token y poder realizar las peticiones
        user = User(
            email='edwinj.gutierrezm@gmail.com',
            first_name='Testing',
            last_name='Testing',
            username='testing_user'
        )
        user.set_password('testingpassword')
        user.save()

        client = APIClient()
        response = client.post(
            '/api/login/',  {
                'username': 'testing_user',
                'password': 'testingpassword'
            }
        )

        result = json.loads(response.content)
        self.access_token = result['access_token']


    def test_create_todo(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        response  = client.post(
            '/api/todos/create',  {
                'description': 'Responde correos',
                'duration': 30,
                'status': 'Pendiente'
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_update_todo(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        todo = Todo.objects.create(
            description='Preparar la cena',
            duration=40,
            status='Pendiente'
        )

        test_todo_update = {
            'description': 'Preparar la cena',
            'duration': 40,
            'status': 'Completada',
            'recorded_time': 20
        }

        response = client.put(
            f'/api/todos/{todo.pk}/update',
            test_todo_update
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test para editar despues de que la tarea ya se encuentra completada
        test_todo_update['status'] = 'Pendiente'

        response = client.put(
            f'/api/todos/{todo.pk}/update',
            test_todo_update
        )

        self.assertEqual(response.data, 'La tarea ya se encuentra completada')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_todo(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        todo = Todo.objects.create(
            description='Preparar la cena',
            duration=40,
            status='Pendiente'
        )

        response = client.delete(
            f'/api/todos/{todo.pk}/delete'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        todo_exists = Todo.objects.filter(pk=todo.pk)
        self.assertFalse(todo_exists)


