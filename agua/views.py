from rest_framework import viewsets,generics
from .models import Agua, UserGoals
from garrafon.models import Garrafon
from .serializers import AguaSerializer,TotalSerializer,WeekSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db.models import Sum
import locale
class CreateAgua(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AguaSerializer

    def create(self, request, *args,**kwargs):
        data = request.data.copy()
        #Hard code garrafon and botella 
        data['user'] = self.request.user.pk
        data['garrafon'] = 1
        data['botella'] = 1
        
        #get garrafon and update current amount
        try:
            curGarrafon = Garrafon.objects.get(id=1)
        except Garrafon.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        newValue = curGarrafon.cantidad- float(request.data['cantidad'])
        if newValue < 0:
            newValue = 0
        
        curGarrafon.__dict__.update(cantidad = newValue)
        curGarrafon.save()

        #get all user water from today to check goal
        try:
            todayTotalWater = Agua.objects.filter(user=self.request.user, created_at__gte=timezone.now().date()).aggregate(cantidad=Sum('cantidad'))
            #update cur goal
            if not todayTotalWater['cantidad']:
                todayTotalWater['cantidad'] = float(request.data['cantidad'])
            else:
                todayTotalWater['cantidad'] += float(request.data['cantidad'])
            userGoal = UserGoals.objects.get(user=self.request.user)

            if (todayTotalWater['cantidad'] >= (userGoal.currentGoal / 1000) and 
                userGoal.updated_at.date() < timezone.now().date() ):

                userGoal.__dict__.update(daysAchieved = userGoal.daysAchieved + 1)
                userGoal.save()

        except UserGoals.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        #Add new water entry
        serializer = AguaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyAguaSemana(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WeekSerializer

    def get(self, request, *args,**kwargs):
        today = timezone.now()
        seven_day_before = today - timedelta(days=6)
        curUser = self.request.user
        allWeekEntries = Agua.objects.filter(user=curUser,created_at__gte=seven_day_before).order_by('created_at')
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        #seperate total by days of week
        daysHashMap = {}
        prevDays = seven_day_before
        for i in range(7):
            daysHashMap[prevDays.strftime("%A")] = 0
            prevDays = prevDays + timedelta(days=1)

        for obj in allWeekEntries:
            daysHashMap[obj.created_at.strftime("%A")] += float(obj.cantidad)

        total = 0
        for k, v in daysHashMap.items():
            total += v
        promedioSemanal = round(total / 7, 2)
        hoy = round(daysHashMap[str(date.today().strftime("%A"))],2)
        serializer = WeekSerializer(data={'hoy':hoy, 'promedioSemanal':promedioSemanal, 'semana':daysHashMap})

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        

class UserStadistics(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TotalSerializer

    def get(self, request, *args,**kwargs):
        curUser = self.request.user        
        total = Agua.objects.filter(user=curUser).aggregate(cantidad=Sum('cantidad'))
        userGoal = UserGoals.objects.get(user=curUser)
        todayTotal = Agua.objects.filter(user=self.request.user, created_at__gte=timezone.now().date()).aggregate(cantidad=Sum('cantidad'))
        serializer = TotalSerializer(
            data={'cantidad': round(total['cantidad'],2), 
            'daysAchieved':userGoal.daysAchieved,
            'todayTotal': 0 if not todayTotal['cantidad'] else todayTotal['cantidad']}
            )
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




