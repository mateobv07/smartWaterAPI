from django.urls import include, path
from agua import views


urlpatterns = [
    path('myTotal/', views.UserTotalWater.as_view()),
    path('myWeek/', views.MyAguaSemana.as_view()),
    path('create/', views.CreateAgua.as_view())
]