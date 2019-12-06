from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from web_gpio.models import Raspi_GPIO
from web_gpio.serializers import RaspiGPIOSerializer

import RPi.GPIO as GPIO


def rpi_gpio_setup(pin_num, pin_state):
    """Setup GPIO pins as dictated by its pin state"""
    # Initial raspberry pi GPIO setup
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # Set raspberry pi GPIO pins high/low
    GPIO.setup(pin_num, GPIO.OUT)
    if pin_state:
        GPIO.output(pin_num, GPIO.HIGH)
    else:
        GPIO.output(pin_num, GPIO.LOW)


def index(request):
    """Setup raspberry pi's GPIO pins and render index page"""
    # Get pin numbers and current set state from database
    pins = { pin.pin_number : pin.state for pin in Raspi_GPIO.objects.all() }
    for pin_num, pin_state in pins.items():
        rpi_gpio_setup(pin_num, pin_state)
    return render(request, 'web_gpio/index.html')


def rpi_gpio(request):
    if request.method == 'GET':
        pin = Raspi_GPIO.objects.get(pk=request.GET['button_id'])
        pin.state = not pin.state
        pin.save()
        GPIO.output(pin.pin_number, pin.state)
    return HttpResponse()


class RaspiGPIOList(APIView):
    """List all Raspi_GPIO instances as JSON"""

    def get(self, request):
        rpi_gpio = Raspi_GPIO.objects.all()
        serializer = RaspiGPIOSerializer(rpi_gpio, many=True)
        return Response(serializer.data)


class RaspiGPIODetail(APIView):
    """Retrieve and update a Raspi_GPIO instance"""

    def get(self, request, pk):
        """HTTP GET method to retrieve specific object"""
        rpi_gpio = get_object_or_404(Raspi_GPIO, pk=pk)
        serializer = RaspiGPIOSerializer(rpi_gpio)
        return Response(serializer.data)

    def put(self, request, pk):
        """HTTP PUT method to update pin state of object in database"""
        rpi_gpio = get_object_or_404(Raspi_GPIO, pk=pk)
        serializer = RaspiGPIOSerializer(rpi_gpio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Retrieve object's pin number and its new output state
            rpi_gpio = Raspi_GPIO.objects.get(pk=pk)
            rpi_gpio_setup(rpi_gpio.pin_number, rpi_gpio.state)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

