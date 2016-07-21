
from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

class ThermoInfo(models.Model):
    temperature = models.FloatField(verbose_name="Temperatura")
    local = models.CharField(verbose_name="Local", max_length=150)
    device_ip = models.CharField(
        verbose_name="Ip do dispositivo", max_length=15)
    capture_data = models.DateTimeField(
        verbose_name="Data de Captura", default=timezone.now)

    class Meta:
        verbose_name = (u'Thermo Info')
        verbose_name_plural = (u"Thermo Info's")
