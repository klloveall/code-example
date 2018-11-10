from django.urls import path

from weather import views

urlpatterns = [
    path('weather/', views.average_temp_form, name="weather_form"),
    path('weather/api/v1/', views.average_temp_view, name="weather_api"),
]
