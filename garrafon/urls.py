
from django.urls import include, path
from garrafon import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.GarrafonViewSet)

urlpatterns = [
    path('my/', views.MyGarrafones.as_view()),
    path('updateOne/', views.UpdateOneGarrafon.as_view()),
    path('', include(router.urls)),
]
