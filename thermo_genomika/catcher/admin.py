
from django.contrib import admin
from .models import ThermoInfo

class ThermoInfoAdmin(admin.ModelAdmin):
    search_fields = ['local', 'capture_data', 'temperature']
    list_display = (
        'temperature',
        'local',
        'device_ip',
        'capture_data'
    )

admin.site.register(ThermoInfo, ThermoInfoAdmin)
