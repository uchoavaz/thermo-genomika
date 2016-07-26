
from django.contrib import admin
from .models import ThermoInfo
from .models import AllowedAddress
from .models import ThermoLog


class ThermoInfoAdmin(admin.ModelAdmin):
    search_fields = ['local', 'capture_date', 'temperature', 'device_ip__ip']
    list_display = (
        'temperature',
        'local',
        'device_ip',
        'capture_date'
    )


class AllowedAddressAdmin(admin.ModelAdmin):
    search_fields = ['ip', 'is_active', 'measure', 'max_temperature', 'days_to_delete']
    list_display = (
        'ip',
        'max_temperature',
        'days_to_delete',
        'measure',
        'is_active',
    )


class ThermoLogAdmin(admin.ModelAdmin):
    search_fields = ['request', 'log', 'device_ip', 'capture_date']
    list_display = (
        'request',
        'log',
        'device_ip',
        'capture_date',
    )

admin.site.register(ThermoLog, ThermoLogAdmin)
admin.site.register(ThermoInfo, ThermoInfoAdmin)
admin.site.register(AllowedAddress, AllowedAddressAdmin)
