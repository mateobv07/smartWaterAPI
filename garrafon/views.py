from rest_framework import viewsets, generics
from .models import Garrafon
from rest_framework.response import Response
from rest_framework import status

from .serializers import GarrafonSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User
from .serializers import CurrentUserSerializer, RegisterSerializer


# Create your views here.
class GarrafonViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Garrafon.objects.all()
    serializer_class = GarrafonSerializer

class MyGarrafones(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GarrafonSerializer
    def get_queryset(self):
        curUser = self.request.user
        return Garrafon.objects.filter(user=curUser)

    def create(self, request, *args,**kwargs):
        data = request.data.copy()
        data['user'] = self.request.user.pk
        serializer = GarrafonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateOneGarrafon(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GarrafonSerializer
    def update(self, request, *args, **kwargs):
        try:
            curGarrafon = Garrafon.objects.get(id=request.data['id'])
        except Garrafon.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        curGarrafon.__dict__.update(cantidad = request.data['cantidad'])
        curGarrafon.__dict__.update(name = request.data['name'])
        curGarrafon.save()
        return Response(status=status.HTTP_200_OK)

class CurrentUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer