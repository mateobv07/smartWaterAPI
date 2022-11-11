
from django.urls import include, path
from botella import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.BotellaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
