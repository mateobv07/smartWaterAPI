from .models import Agua
from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class AguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agua
        fields = '__all__'

class TotalSerializer(serializers.Serializer):
    cantidad = serializers.FloatField()
    daysAchieved = serializers.IntegerField()
    todayTotal = serializers.FloatField()

class WeekSerializer(serializers.Serializer):
    hoy = serializers.FloatField()
    promedioSemanal = serializers.FloatField()
    semana = serializers.DictField()