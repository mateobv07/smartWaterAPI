from django.shortcuts import render
from rest_framework import viewsets
from .models import Botella
from .serializers import BotellaSerializer

# Create your views here.
class BotellaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Botella.objects.all()
    serializer_class = BotellaSerializer