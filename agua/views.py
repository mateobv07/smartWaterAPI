from rest_framework import viewsets,generics
from .models import Agua
from garrafon.models import Garrafon
from .serializers import AguaSerializer,TotalSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum

class CreateAgua(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AguaSerializer

    def create(self, request, *args,**kwargs):
        data = request.data.copy()
        #Hard code garrafon and botella 
        data['user'] = self.request.user.pk
        data['garrafon'] = 2
        data['botella'] = 2
        
        try:
            curGarrafon = Garrafon.objects.get(id=2)
        except Garrafon.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        newValue = curGarrafon.cantidad- float(request.data['cantidad'])
        if newValue < 0:
            newValue = 0
            
        curGarrafon.__dict__.update(cantidad = newValue)
        curGarrafon.save()

        serializer = AguaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyAguaSemana(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AguaSerializer

    def get_queryset(self):
        today = timezone.now()
        seven_day_before = today - timedelta(days=7)
        curUser = self.request.user
        return Agua.objects.filter(user=curUser,created_at__gte=seven_day_before)

class UserTotalWater(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TotalSerializer

    def get(self, request, *args,**kwargs):
        curUser = self.request.user        
        total = Agua.objects.filter(user=curUser).aggregate(cantidad=Sum('cantidad'))
        serializer = TotalSerializer(data=total)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




