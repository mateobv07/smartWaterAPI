from django.shortcuts import render
from rest_framework import viewsets
from .models import Agua
from .serializers import AguaSerializer

# Create your views here.
class AguaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Agua.objects.all()
    serializer_class = AguaSerializer
