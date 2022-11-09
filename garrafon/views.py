from rest_framework import viewsets, generics
from .models import Garrafon

from .serializers import GarrafonSerializer
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from .serializers import CurrentUserSerializer, RegisterSerializer


# Create your views here.
class GarrafonViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Garrafon.objects.all()
    serializer_class = GarrafonSerializer
        
class CurrentUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer