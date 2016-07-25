
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import ThermoInfo
from .models import AllowedAddress
from .models import ThermoLog
from ipware.ip import get_ip
from mailer.tasks import mail
from .tasks import delete_old_records


class CatcherView(TemplateView):

    def get(self, request, *args, **kwargs):
        log = ''
        request = self.request
        ip = get_ip(request)
        try:
            temperature = request.GET.get('temp')
            local = request.GET.get('local')
            if temperature is None:
                raise Exception("Temperature is not in request")

            if local is None:
                raise Exception("Local is not in request")

            temperature = float(temperature) / 1000
            log = 'Request received'
            allowed_address = AllowedAddress.objects.get(ip=ip)
            if allowed_address.is_active:

                thermo_info = ThermoInfo.objects.create(
                    temperature=temperature,
                    local=local,
                    device_ip=allowed_address
                )
                log = log + ", "'Data saved with success'
                email_log = mail(thermo_info, local, temperature)
                log = log + ", " + email_log
                delete_log = delete_old_records(ip)
                log = log + ", " + delete_log
            else:
                log = log + ", " + "No device active"

        except ObjectDoesNotExist as err:
            log = log + ", " + err

        except TypeError as err:
            log = log + ", " + err

        except Exception as err:
            log = log + ", " + ("Error:" + str(err))

        ThermoLog.objects.create(
            request=request,
            log=log,
            device_ip=ip
        )
        return HttpResponse('')


catcher = CatcherView.as_view()
