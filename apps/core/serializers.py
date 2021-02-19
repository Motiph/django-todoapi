from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields  = '__all__'

