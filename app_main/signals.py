import threading

from crum import get_current_request
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save
from django.dispatch import receiver

from FitnessArmyMVC.utils import create_mail, get_host_url
from app_main.models import Contact, Config


def async_email(instance, request):
    current_site = get_current_site(request)
    subject = 'Contacto realizado ' + current_site.domain
    mail = create_mail(instance.email, subject, 'mails/contact.html', {
        'host': get_host_url(request),
        "domain": current_site.domain,
        'name': instance.name,
        'cfg': Config.objects.first() if Config.objects.exists() else None
    })
    mail.send()
    print('Se envió un correo a contacto')


@receiver(post_save, sender=Contact)
def send_contact_email(sender, instance: Contact, created, **kwargs):
    if created:
        request = get_current_request()
        thread = threading.Thread(target=async_email, args=(instance, request))
        thread.start()
