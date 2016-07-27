
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import ListView
from catcher.models import ThermoInfo
from catcher.models import AllowedAddress
from django.contrib import messages
from django.utils import timezone



class HomeView(TemplateView):
    template_name = "home.html"


class ChartsView(ListView):
    template_name = "charts.html"
    model = ThermoInfo
    message_error = ''
    message_ok = ''

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET:

            return redirect(reverse_lazy('core:charts'))

        else:
            return super(
                ChartsView, self).dispatch(
                request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(ChartsView, self).get_queryset()
        request = self.request.GET
        if request:
            local = request.get('local')
            if local == '':
                messages.error(
                    self.request, u"Local não especificado")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)
        queryset = self.get_queryset().order_by('capture_date')
        try:
            context['room'] = 'Teste'
        except IndexError:
            context['room'] = 'sala 1'
        context['date_list'] = self.get_date_list_string(queryset)
        context['temp_list'] = self.get_temp_list_string(queryset)
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
