
from __future__ import unicode_literals
from django.utils import timezone


from django.db import models


class MailLog(models.Model):
    local = models.CharField(verbose_name='Local', max_length=150, default='')
    temperature = models.FloatField(verbose_name='Temperature', default=20)
    situation = models.CharField(verbose_name='Situation', max_length=20)
    recipient_list = models.TextField(
        verbose_name='Recipient list', blank=True)
    date = models.DateTimeField(
        verbose_name="Date", default=timezone.now)

    class Meta:
        verbose_name = (u'Mails Logs')
        verbose_name_plural = (u"Mail Log")


class Recipient(models.Model):
    email = models.EmailField(verbose_name="E-mail")
    is_active = models.BooleanField(verbose_name='Is active ?', default=False)

    class Meta:
        verbose_name = (u'Recipients')
        verbose_name_plural = (u"Recipient")
