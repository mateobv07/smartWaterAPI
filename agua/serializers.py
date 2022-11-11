from .models import Agua
from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class AguaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agua
        fields = '__all__'