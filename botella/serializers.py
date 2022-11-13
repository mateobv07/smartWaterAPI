
from .models import Botella
from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class BotellaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Botella
        fields = '__all__'
