from django.shortcuts import render
from rest_framework import viewsets,generics
from .models import Botella
from .serializers import BotellaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class BotellaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Botella.objects.all()
    serializer_class = BotellaSerializer

class UpdateOneBotella(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BotellaSerializer
    def update(self, request, *args, **kwargs):
        try:
            curBotella = Botella.objects.get(id=request.data['id'])
        except Botella.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        curBotella.__dict__.update(name = request.data['name'])
        curBotella.save()
        return Response(status=status.HTTP_200_OK)

class MyBotellas(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BotellaSerializer

    def get_queryset(self):
        curUser = self.request.user
        return Botella.objects.filter(user=curUser)

    def create(self, request, *args,**kwargs):
        data = request.data.copy()
        data['user'] = self.request.user.pk
        serializer = BotellaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
