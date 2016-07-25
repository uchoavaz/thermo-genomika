
from mailer.models import MailLog
from mailer.models import Recipient
from mailer.mail import send_mail


def mail(thermo_info, local, temperature):
    email_log = 'Email sent with success'
    if thermo_info.device_ip.max_temperature < temperature:

        situation = "ALARME !"
        recipient_list = Recipient.objects.filter(
            is_active=True).values_list('email', flat=True)
        if len(recipient_list) > 0:
            send_mail(local, temperature, situation, recipient_list)

        else:
            email_log = "No e-mails no send"
        MailLog.objects.create(
            local=local,
            temperature=temperature,
            situation=situation,
            recipient_list=', '.join(recipient_list)
        )
    else:
        email_log = ""
        return email_log

    return email_log
