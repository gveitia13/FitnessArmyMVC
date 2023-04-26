import threading
from os.path import splitext

from crum import get_current_request
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save
from django.dispatch import receiver

from FitnessArmyMVC.utils import create_mail, get_host_url
from app_main.models import Contact, Config, Product, Subscriptor


def async_email(instance, request):
    current_site = get_current_site(request)
    subject = 'Contacto realizado ' + current_site.domain
    mail = create_mail([instance.email], subject, 'mails/contact.html', {
        'host': get_host_url(request),
        "domain": current_site.domain,
        'name': instance.name,
        'cfg': Config.objects.first() if Config.objects.exists() else None
    })
    mail.send()
    print('Se envió un correo a contacto')


def async_email_product(instance: Product, request):
    current_site = get_current_site(request)
    subject = 'Nuevo producto ' + current_site.domain
    message = instance.create_message_product()
    cfg = Config.objects.first() if Config.objects.exists() else None

    mail = create_mail([i.email for i in Subscriptor.objects.all()], subject, 'mails/product.html', {
        'host': get_host_url(request),
        "domain": current_site.domain,
        'message': message,
        'cfg': cfg,
        'product': instance,
    })
    image = open(instance.image.path, 'rb')
    image_path_name, ext = splitext(instance.image.name)
    index = image_path_name.rfind('/')
    image_name = image_path_name[index + 1:] if index else image_path_name

    mail.attach(f'{image_name}{ext}', image.read(), f'image/{ext}')
    mail.send()
    print('Se envió un correo a producto')


@receiver(post_save, sender=Contact)
def send_contact_email(sender, instance: Contact, created, **kwargs):
    if created:
        request = get_current_request()
        thread = threading.Thread(target=async_email, args=(instance, request))
        thread.start()


@receiver(post_save, sender=Product)
def send_contact_email(sender, instance: Product, created, **kwargs):
    if created:
        request = get_current_request()
        thread = threading.Thread(target=async_email_product, args=(instance, request))
        thread.start()
