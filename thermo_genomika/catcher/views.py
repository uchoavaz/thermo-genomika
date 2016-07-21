from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import ThermoInfo
from ipware.ip import get_ip


class CatcherView(TemplateView):
    def get(self, request, *args, **kwargs):
        ip = get_ip(self.request)
        request = self.request.GET
        temperature = float(request.get('temp')) / 1000
        local = request.get('local')
        ThermoInfo.objects.create(
            temperature=temperature,
            local=local,
            device_ip=ip
        )
        return HttpResponse('')

catcher = CatcherView.as_view()
