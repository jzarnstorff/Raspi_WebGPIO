from django.db import models

class Raspi_GPIO(models.Model):
    """Raspberry Pi physical GPIO pin number and its on/off state"""
    pin_number = models.PositiveSmallIntegerField()
    state = models.BooleanField(default=False)
