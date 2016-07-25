
from .models import AllowedAddress
from .models import ThermoInfo
from .models import ThermoLog
from django.utils import timezone
import datetime


def delete_old_records(ip):

    days_to_delete = AllowedAddress.objects.get(ip=ip).days_to_delete
    days_ago = (timezone.now() - datetime.timedelta(days=days_to_delete))

    ThermoInfo.objects.filter(
        capture_date__lte=days_ago, device_ip__ip=ip).delete()
    ThermoLog.objects.filter(
        capture_date__lte=days_ago, device_ip=ip).delete()
