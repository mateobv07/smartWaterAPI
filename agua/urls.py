from django.urls import include, path
from agua import views


urlpatterns = [
    path('myStadistics/', views.UserStadistics.as_view()),
    path('myWeek/', views.MyAguaSemana.as_view()),
    path('create/', views.CreateAgua.as_view())
]