from django.urls import path
from web_gpio import views

urlpatterns = [
        path('', views.index, name='index'),
        path('rpi_gpio/', views.rpi_gpio, name='rpi_gpio'),
        path('rpi_gpio/api/', views.RaspiGPIOList.as_view(), name='api_list'),
        path('rpi_gpio/api/<int:pk>/', views.RaspiGPIODetail.as_view(), name='api_detail'),
        ]
