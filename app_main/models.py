import uuid

from django.core.mail import send_mail
from django.db import models
from django.forms import model_to_dict
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

from FitnessArmyMVC import settings
from FitnessArmyMVC.settings import STATIC_URL


class Config(SingletonModel):
    name = models.CharField('Nombre', max_length=50)
    email = models.EmailField(_("email address"), unique=True)
    address = models.CharField('Dirección', max_length=200, null=True, blank=True)
    phone_number = models.CharField('Teléfono', unique=True, null=True, blank=True, max_length=15, error_messages={
        'unique': 'Ya este teléfono está registrado'}, help_text='Poner el código del país')
    # google_maps = models.CharField(max_length=900, verbose_name='Mapa de google')
    # social networks
    instagram = models.URLField('Link de Instagram', null=True, blank=True, )
    facebook = models.URLField('Link de Facebook', null=True, blank=True, )
    twitter = models.URLField('Link de Twitter', null=True, blank=True, )
    whatsapp = models.CharField('Número de Whatsapp', null=True, blank=True, max_length=150)
    # telegram = models.CharField('Link de telegram', null=True, blank=True, max_length=100)
    # Pagos
    # mlc = models.CharField('Tarjeta MLC', validators=[MinLengthValidator(16), validate_only_numbers], max_length=16,
    #                        unique=True, null=True, blank=True)
    # cup = models.CharField('Tarjeta CUP', validators=[MinLengthValidator(16), validate_only_numbers], max_length=16,
    #                        unique=True, null=True, blank=True)
    # Fotos
    logo = models.ImageField('Logo', upload_to='config/logo/')
    icon = models.ImageField('Ícono', upload_to='config/icon/')
    banner = models.ImageField('Banner', upload_to='config/banner/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Configuración'
        verbose_name_plural = 'Configuraciones'

    # def get_logo(self):
    #     if self.logo:
    #         return self.logo.url
    #     return f'{settings.STATIC_URL}img/empty.png'

    def get_logo(self):
        return mark_safe(f'<a href="{self.logo.url}"><img src="{self.logo.url}" class="agrandar mb-2 mr-2" '
                         f'height="60" /></a>')

    def get_icon(self):
        return mark_safe(f'<a href="{self.icon}"><img src="{self.icon}" class="agrandar mb-2 mr-2" '
                         f'height="60" /></a>')

    def get_banner(self):
        return mark_safe(f'<a href="{self.banner}"><img src="{self.banner}" class="agrandar mb-2 mr-2" '
                         f'height="60" /></a>')

    get_logo.short_description = 'Vista previa'
    get_icon.short_description = 'Vista previa'
    get_banner.short_description = 'Vista previa'


class Product(models.Model):
    image = models.ImageField(upload_to='product/img', verbose_name='Imagen')
    name = models.CharField(max_length=150, verbose_name='Nombre')
    price = models.DecimalField(max_digits=9, verbose_name='Precio', decimal_places=2, )
    info = models.TextField('Información', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Visible')
    is_important = models.BooleanField('Destacado', default=False)
    sales = models.PositiveIntegerField(verbose_name='Ventas', default=0)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.image.url
        item['info'] = self.info_tag()
        item['price'] = float(self.price)
        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def info_tag(self):
        return self.info

    def img_link(self):
        if self.image:
            return mark_safe(
                f'<a href="{self.image.url}"><img src="{self.image.url}" class="agrandar mb-2 mr-2" '
                f'height="70" /></a>')
        return mark_safe(
            f'<a href="{STATIC_URL}img/empty.png"><img src="{STATIC_URL}img/empty.png" class="agrandar mb-2 mr-2" '
            f'height="70" /></a>')

    img_link.short_description = 'Vista previa'
    info_tag.short_description = 'Información'

    def create_message_product(self):
        message = f'<b>Nombre:</b> {self.name}<br>'
        message += f'<b>Precio:</b> {self.price}<br>'
        if self.info:
            message += f'<b>Descripción:</b> {self.info}<br>'
        return message


class Property(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    text = models.CharField('Característica', max_length=120)

    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'

    def __str__(self): return self.text


class Contact(models.Model):
    name = models.CharField('Nombre y apellidos', max_length=200)
    email = models.EmailField(_("email address"))
    message = models.TextField('Mensaje')
    phone_number = models.CharField('Teléfono', null=True, blank=True, max_length=15,
                                    help_text='Poner el código del país')
    is_attended = models.BooleanField('Está atendido', default=False)

    def __str__(self): return f'Contacto {self.email}'

    class Meta:
        verbose_name = 'Contacto'
        ordering = ['is_attended']


class Subscriptor(models.Model):
    email = models.EmailField(_("email address"), unique=True)

    def __str__(self):
        return f'Suscriptor {self.email}'

    class Meta:
        verbose_name_plural = 'Subscriptores'


class Orden(models.Model):
    link_de_pago = models.CharField(max_length=500, null=True, blank=True)
    total = models.FloatField(default=0, verbose_name='Importe total')
    uuid = models.UUIDField(verbose_name='ID', primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField('Estado', choices=(
        ('1', 'Completada'),
        # ('2', 'Pendiente'),
        ('3', 'Cancelada'),
    ), max_length=10, default='2')
    date_created = models.DateTimeField('Fecha', auto_now_add=True, )
    # Campos del form
    name = models.CharField('Nombre', max_length=200)
    phone_number = models.CharField('Teléfono', max_length=200, null=True, blank=True)
    email = models.EmailField('Correo')
    address = models.CharField('Dirección', max_length=900)

    def __str__(self):
        return '{}'.format(str(self.uuid))

    def get_total(self):
        return '{:.2f}'.format(self.total)

    def get_componente(self):
        return mark_safe(''.join(['•' + i.__str__() + '<br>' for i in self.componente_orden.all()]))

    def get_cancel_link(self):
        if self.status != '3':
            return mark_safe(
                f'<a href="{reverse_lazy("cancelar", kwargs={"pk": self.pk})}" class="btn btn-danger rounded-pill '
                f'">Cancelar<a/>')
        else:
            return ''

    def get_status(self):
        return mark_safe(
            f'<span class="text-{"success" if self.status == "1" else "danger"}">{self.get_status_display()}</span>')

    get_total.short_description = 'Importe total'
    get_cancel_link.short_description = 'Opciones'
    get_componente.short_description = 'Componentes'
    get_status.short_description = 'Estado'

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ('-date_created', '-status',)

    def toJSON(self):
        item = model_to_dict(self)
        item['date_created'] = self.date_created.strftime('%d-%m-%Y')
        item['uuid'] = str(self.uuid)
        item['componentes'] = [i.toJSON() for i in self.componente_orden.all()]
        return item


class ComponenteOrden(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='componente_producto')
    respaldo = models.FloatField()
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='componente_orden')
    cantidad = models.IntegerField()

    def __str__(self):
        return mark_safe(
            '{}x - {} - {}'.format(self.cantidad, self.producto.name if self.producto else "Producto eliminado",
                                   '$<b>{:.2f}</b>'.format(self.respaldo), ))

    def Componente(self):
        return str(self)

    def toJSON(self):
        item = model_to_dict(self, exclude=['orden'])
        return item

    class Meta:
        ordering = ('orden', 'producto')
        verbose_name = 'Componente de venta'
        verbose_name_plural = 'Componentes de ventas'


class Offer(models.Model):
    subject = models.CharField('Asunto', max_length=120)
    message = models.TextField('Mensaje')
    date_created = models.DateTimeField('Fecha', auto_now_add=True, )
    status = models.CharField('Estado', choices=(
        ('1', 'Enviada'),
        ('2', 'No enviada'),
    ), max_length=2, default='2')

    class Meta:
        verbose_name = 'Oferta'
        ordering = ('status', 'date_created',)

    def __str__(self): return self.subject + ' ' + str(self.date_created)

    def get_status(self):
        return mark_safe(
            f'<span class="text-{"success" if self.status == "1" else "danger"}">{self.get_status_display()}</span>')

    get_status.short_description = 'Estado'

    def send_offer_mail(self):
        send_mail(self.subject, self.message, settings.EMAIL_HOST_USER, [i.email for i in Subscriptor.objects.all()])
