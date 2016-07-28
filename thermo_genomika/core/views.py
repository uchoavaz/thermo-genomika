
# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.views.generic import ListView
from catcher.models import ThermoInfo
from catcher.models import AllowedAddress
from django.contrib import messages
from django.utils import timezone
from django.db.models import Max
from django.db.models import Min


class HomeView(TemplateView):
    template_name = "home.html"


class ChartsView(ListView):
    template_name = "charts.html"
    model = ThermoInfo

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)
        request = self.request.GET

        local_pk = request.get('local_pk')
        local_name = 'Genomika'
        date_list = []
        temp_list = []
        qtd_temp = 0
        max_temp = '-'
        min_temp = '-'
        last_temp = '-'

        if self.request.GET:

            try:
                allowed_address = AllowedAddress.objects.get(pk=int(local_pk))
                queryset = self.get_queryset().filter(
                    device_ip=allowed_address).order_by('capture_date')
                local_name = allowed_address.local
                date_list = self.get_date_list_string(queryset)
                temp_list = self.get_temp_list_string(queryset)
                qtd_temp = queryset.count()

                measure = allowed_address.get_measure_display()
                temp = queryset.aggregate(
                    Max('temperature'))['temperature__max']
                if temp is not None:
                    max_temp = str(temp) + " " + measure

                temp = queryset.aggregate(
                    Min('temperature'))['temperature__min']

                if temp is not None:
                    min_temp = str(temp) + " " + measure

                try:
                    last_position = queryset[len(queryset) - 1]
                    last_temp = str(last_position.temperature) + " " + measure
                except AssertionError:
                    pass

            except (ValueError, ObjectDoesNotExist):
                messages.error(
                    self.request, 'Local inexistente')
            except TypeError:
                messages.error(
                    self.request, 'Insira um Local')

        context['last_temp'] = last_temp
        context['min_temp'] = min_temp
        context['max_temp'] = max_temp
        context['qtd_temp'] = qtd_temp
        context['local_name'] = local_name
        context['date_list'] = date_list
        context['temp_list'] = temp_list
        context['room_list'] = AllowedAddress.objects.all().distinct('local')

        return context

    def get_date_list_string(self, queryset):
        date_list = []
        for query in queryset:
            date = timezone.localtime(query.capture_date)
            date = date.strftime('%d-%m-%Y %H:%M')
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
