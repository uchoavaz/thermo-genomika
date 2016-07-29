
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.generic import ListView
from catcher.models import ThermoInfo
from catcher.models import AllowedAddress
from django.contrib import messages
from django.utils import timezone
from django.db.models import Max
from django.db.models import Min
from datetime import datetime
import csv


def correct_date_get_request(request, start_date, end_date):
    try:
        start_date = datetime.strptime(start_date, "%d/%m/%Y")
    except (ValueError, UnicodeEncodeError):
        messages.error(
            request,
            u'Data início incorreta')
        start_date = ''

    if end_date != '':
        try:
            end_date = datetime.strptime(end_date, "%d/%m/%Y")
        except (ValueError, UnicodeEncodeError):
            messages.error(
                request, 'Data fim incorreta')
            end_date = ''

    if start_date != '' and end_date != '' \
            and (end_date - start_date).days < 0:
        raise Exception(
            u'Data fim maior que a data início')

    return {'start_date': start_date, 'end_date': end_date}


class HomeView(ListView):
    template_name = "home.html"
    model = ThermoInfo

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['registered_thermos'] = AllowedAddress.objects.all().count()
        context['total_temp'] = self.get_queryset().count()
        context['qtd_not_allowed_temp'] = self.get_queryset().filter(
            allowed_temp=False).count()
        return context


class ChartsView(ListView):
    template_name = "charts.html"
    model = ThermoInfo

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)
        request = self.request.GET

        local_name = 'Genomika'
        date_list = []
        temp_list = []
        qtd_temp = 0
        max_temp = '-'
        min_temp = '-'
        last_temp = '-'
        start_date_begin = ''
        end_date_begin = ''

        if request:
            local_pk = request.get('local_pk')
            start_date = request.get('start_date')
            end_date = request.get('end_date')

            start_date_begin = start_date
            end_date_begin = end_date
            try:

                get = correct_date_get_request(
                    self.request, start_date, end_date)
                start_date = get['start_date']
                end_date = get['end_date']

                allowed_address = AllowedAddress.objects.get(pk=int(local_pk))
                queryset = self.get_queryset().filter(
                    device_ip=allowed_address)
                if start_date != '':
                    queryset = queryset.filter(capture_date__gte=start_date)
                if end_date != '':
                    queryset = queryset.filter(capture_date__lte=end_date)
                queryset = queryset.order_by('capture_date')
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
            except Exception as err:
                messages.error(
                    self.request, err)

        context['start_date'] = start_date_begin
        context['end_date'] = end_date_begin
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


class ReportView(ListView):
    template_name = "reports.html"
    model = ThermoInfo

    def generate_csv(self, file_name, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="{0}_thermo_report_{1}.csv"'.format(
                file_name, datetime.now().strftime("%d_%m_%Y"))

        writer = csv.writer(response, delimiter='|')
        header = [
            ThermoInfo._meta.get_field("temperature").verbose_name.title(),
            ThermoInfo._meta.get_field("allowed_temp").verbose_name.title(),
            ThermoInfo._meta.get_field("device_ip").verbose_name.title(),
            ThermoInfo._meta.get_field("capture_date").verbose_name.title()
        ]
        writer.writerow(header)

        for line in queryset:
            writer.writerow([
                str(line.temperature),
                line.allowed_temp,
                line.device_ip,
                timezone.get_current_timezone().normalize(line.capture_date)
            ])
        return response

    def dispatch(self, request, *args, **kwargs):

        if self.request.GET:
            local_pk = self.request.GET.get('local_pk')
            try:

                allowed_address = AllowedAddress.objects.get(pk=int(local_pk))
                queryset = self.get_queryset().filter(
                    device_ip=allowed_address)
                queryset = queryset.order_by('capture_date')

                return self.generate_csv(allowed_address.local, queryset)
            except (ValueError, ObjectDoesNotExist):
                messages.error(
                    self.request, 'Local inexistente')
            except TypeError:
                messages.error(
                    self.request, 'Insira um Local')
            except Exception as err:
                messages.error(
                    self.request, err)
            return super(
                ReportView, self).dispatch(
                self.request, *args, **kwargs)

        else:
            return super(
                ReportView, self).dispatch(
                self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        context['room_list'] = AllowedAddress.objects.all().distinct('local')
        return context

report = ReportView.as_view()
home = HomeView.as_view()
charts = ChartsView.as_view()
