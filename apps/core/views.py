from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import Todo
from .serializers import TodoSerializer

from random import randint
import dicttoxml
import requests
import json


def customResponse(meta, data):
    if meta['CONTENT_TYPE'] == 'text/xml':
        xml = dicttoxml.dicttoxml(data, attr_type=False)
        return Response(xml, content_type='text/xml', status=status.HTTP_200_OK)
    return Response(data, status=status.HTTP_200_OK)
    

class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            token = Token.objects.get(user=user)
            return Response({'access_token': token.key})
        return Response('Credenciales no validas', status=status.HTTP_401_UNAUTHORIZED)



class TodoCreateAPIView(APIView):
    """
    Vista para crear una tarea
    """

    def post(self, request, format=None):
        todo = request.data
        serializer = TodoSerializer(data=todo)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class TodoListAPIView(APIView):
    """
    Regresa todas las tareas
    """

    def get(self, request, format=None):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return customResponse(request.META, serializer.data)


class TodoUpdateAPIView(generics.UpdateAPIView):
    """
    Vista para editar o completar una tarea, no se puede editar si ya se
    encuentra completada
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status.lower() == 'completada':
            return Response('La tarea ya se encuentra completada', status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


class DeleteTodoAPIView(generics.DestroyAPIView):
    """
    Elimina una tarea
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class SingleTodoAPIView(APIView):
    """
    Vista para traer una sola tarea con la pk
    """

    def get(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=self.kwargs.get('pk'))
        serializer = TodoSerializer(todo)
        return customResponse(request.META, serializer.data)


class TodoListByStatusAPIView(APIView):
    """
    Regresa las tareas por status
    """

    def get(self, request, *args, **kwargs):
        status = self.request.query_params.get('q', None)
        # serializer = {}
        if status is not None:
            todos = Todo.objects.filter(status=status.capitalize())
            serializer = TodoSerializer(todos, many=True)
            return customResponse(request.META, serializer.data)
        return Response('error')


class TodoListByDescriptionAPIView(APIView):
    """
    Regresa las tareas por descripcion
    """

    def get(self, request, *args, **kwargs):
        search = self.request.query_params.get('q', None)
        # serializer = {}
        if search is not None:
            todos = Todo.objects.filter(description__icontains=search)
            serializer = TodoSerializer(todos, many=True)
            return customResponse(request.META, serializer.data)
        return Response('error')




class TodoListCreateAPIView(APIView):
    """
    Crea una lista de tareas
    """
    
    def post(self, request, format=None):
        data = request.data
        serializer = TodoSerializer(data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class CreateList(APIView):
    def get(self, request, format=None):
        r = requests.get('https://jsonplaceholder.typicode.com/todos/')

        todos = []
        for todo in r.json():
            percentage = randint(80, 100)
            duration = randint(30, 60)
            day = randint(10, 18)
            recorded_time = round((duration*percentage) / 100)
            todos.append({
                'created_at': f'2021-02-{day}T02:42:13.232952Z',
                'updated_at': f'2021-02-{day}T02:42:13.232952Z',
                'description': todo['title'],
                'duration': duration,
                'recorded_time': recorded_time,
                'status': 'Completada'

            })
        return Response(todos)




# class TodoListByStatus(generics.ListAPIView):
#     """
#     Regresa las tareas por status
#     """
#     serializer_class = TodoSerializer

#     def get_queryset(self):
#         queryset = Todo.objects.all()
#         search = self.request.query_params.get('q', None)
#         if search is not None:
#             queryset = queryset.filter(status=search.capitalize())
#         return queryset

# http://localhost:5001/api/tasks/search?q=foo).
    # def get(self, request, *args, **kwargs):
    #     status = self.kwargs.get('q')
    #     todos = Todos.objects.filter(status=status)
    #     serializer = TodoSerializer(todo, many=True)
    #     return customResponse(request.META, serializer.data)


        

