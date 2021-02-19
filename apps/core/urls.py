from django.urls import path, include
from rest_framework import routers


from .views import (
    DeleteTodoAPIView,
    SingleTodoAPIView,
    TodoUpdateAPIView,
    TodoCreateAPIView,
    TodoListAPIView,
    TodoListByStatusAPIView,
    TodoListByDescriptionAPIView,
    LoginAPIView,
    TodoListCreateAPIView,
    CreateList
)


urlpatterns = [
    path('todos/', TodoListAPIView.as_view(), name='todos'),
    path('todos/<int:pk>', SingleTodoAPIView.as_view(), name='single-todo'),
    path('todos/create', TodoCreateAPIView.as_view(), name='create'),
    path('todos/<int:pk>/update', TodoUpdateAPIView.as_view(), name='update'),
    path('todos/<int:pk>/delete', DeleteTodoAPIView.as_view(), name='delete'),
    path('todos/status', TodoListByStatusAPIView.as_view(), name='status'),
    path('todos/search', TodoListByDescriptionAPIView.as_view(), name='description'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('todos/create/list', TodoListCreateAPIView.as_view(), name='create-list'),
    path('makejson/', CreateList.as_view(), name='makejson')
]
