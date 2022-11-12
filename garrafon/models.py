from django.db import models
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class Garrafon(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cantidad = models.FloatField(default=None)
    name = models.CharField(max_length=30, default="Name")
    code = models.CharField(max_length=20, default="code123")

    def __str__(self):
        return f"{self.name} - {self.cantidad} Litros"

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)