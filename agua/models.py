from django.db import models
from django.conf import settings
from garrafon.models import Garrafon
from botella.models import Botella

# Create your models here.
class Agua(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    garrafon = models.ForeignKey(Garrafon,on_delete=models.CASCADE,)
    botella = models.ForeignKey(Botella,on_delete=models.CASCADE,)
    cantidad = models.FloatField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserGoals(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    daysAchieved = models.IntegerField(default=None)
    currentGoal = models.IntegerField(default=2400)
    updated_at = models.DateTimeField(auto_now=True)

