from rest_framework import serializers
from web_gpio.models import Raspi_GPIO

class RaspiGPIOSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raspi_GPIO
        fields = '__all__'
        read_only_fields = [ 'pk', 'pin_number' ]
