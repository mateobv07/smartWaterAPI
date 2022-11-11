from django.urls import include, path
from agua import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.AguaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]