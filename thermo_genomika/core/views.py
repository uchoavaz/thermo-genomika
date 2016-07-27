
from django.views.generic import TemplateView
from django.views.generic import ListView
from catcher.models import ThermoInfo
from django.utils import timezone


class HomeView(TemplateView):
    template_name = "home.html"


class ChartsView(ListView):
    template_name = "charts.html"
    model = ThermoInfo

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)
        queryset = self.get_queryset().order_by('capture_date')
        context['room'] = queryset.filter(
            device_ip__ip='192.168.0.20')[0].local
        context['date_list'] = self.get_date_list_string(queryset)
        context['temp_list'] = self.get_temp_list_string(queryset)
        return context

    def get_date_list_string(self, queryset):
        date_list = []
        for query in queryset:
            date = timezone.localtime(query.capture_date)
            date = date.strftime('%Y-%m-%d %H:%M')
            date_list.append(date)

        return date_list

    def get_temp_list_string(self, queryset):
        temp_list = []
        for query in queryset:
            temp = query.temperature
            temp_list.append(temp)

        return temp_list


home = HomeView.as_view()
charts = ChartsView.as_view()
