
from django.urls import include, path
from garrafon import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.GarrafonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
