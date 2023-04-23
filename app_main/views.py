import json

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from rest_framework.decorators import api_view
from rest_framework.response import Response

from FitnessArmyMVC.utils import get_host_url, create_mail
from app_cart.cart import Cart
from app_main.models import Config, Product, Contact, Subscriptor, Orden, ComponenteOrden
from app_main.serializers import ProductSerializer


def get_global_context(request):
    current_site = get_current_site(request)
    cart = Cart(request)
    print(json.dumps(cart.all(), indent=2))
    total = 0
    for item in cart.all():
        total = total + (float(item['product']['price']) * float(item['quantity']))
    print(total)
    return {
        'cfg': Config.objects.first() if Config.objects.exists() else None,
        'product_list': Product.objects.filter(is_active=True),
        'host': get_host_url(request),
        "domain": current_site.domain,
        'product_in_cart': cart.all(),
        'product_in_cart_json': json.dumps(cart.all()),
        'total': total,
    }


class IndexView(generic.ListView):
    template_name = 'pages/start.html'
    model = Product

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_important=True, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Fitness Army | Inicio'
        context['current_url'] = reverse_lazy('index')
        context['inicio'] = True
        context.update(get_global_context(self.request))
        return context


class ProductDetailsView(generic.DetailView):
    model = Product
    template_name = 'pages/product-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        prod = self.get_object(self.queryset)
        context['title'] = f'Fitness Army | {prod.name}'
        context['current_url'] = reverse_lazy('index')
        context.update(get_global_context(self.request))
        return context


class CatalogView(generic.ListView):
    model = Product
    template_name = 'pages/catalog.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = get_global_context(self.request)
        context.update(super().get_context_data())
        context['title'] = 'Fitness Army | Catálogo'
        context['current_url'] = reverse_lazy('index')
        context['catalog'] = True
        context['high_price'] = Product.objects.filter(is_active=True).order_by('price')[0].price
        return context


class ContactView(generic.CreateView):
    model = Contact
    template_name = 'pages/contact.html'
    fields = '__all__'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = get_global_context(self.request)
        context.update(super().get_context_data())
        context['title'] = 'Fitness Army | Contacto'
        context['current_url'] = reverse_lazy('index')
        context['contact'] = True
        return context

    def post(self, request, *args, **kwargs):
        messages.success(request,
                         'Se ha enviado una notificación por correo, un administrador se pondrá en contacto con usted.')
        return super().post(request, *args, **kwargs)


class CartView(generic.TemplateView):
    template_name = 'pages/cart.html'

    def get_context_data(self, **kwargs):
        context = get_global_context(self.request)
        context.update(super().get_context_data())
        context['title'] = 'Fitness Army | Carrito de compras'
        context['current_url'] = reverse_lazy('index')
        context['carrito'] = True
        return context

    @method_decorator(csrf_exempt, require_POST)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            orden = create_order(request, **{})
            if orden:
                mensaje = create_message_order(request, orden)
                # Sacar alert
                messages.success(request,
                                 'Su orden de compra ha sido realizada, se ha enviado un correo con los detalles')
                import threading
                thread = threading.Thread(target=send_email_order, args=(request, orden, mensaje))
                thread.start()
                return redirect('index')
        return redirect('index')


@method_decorator(csrf_exempt, require_POST)
def subscribe(request):
    email = request.POST['email']
    try:
        sub = Subscriptor.objects.create(email=email)
    except Exception as e:
        print(str(e))
        if str(e).__contains__('UNIQUE'):
            messages.error(request,
                           f'Ha ocurrido un error! El correo {email} ya se encuentra subscrito.')
        else:
            messages.error(request, f'Ha ocurrido un error en el servidor!')
        return redirect(reverse('index'))

    # Send confirmation email
    current_site = get_current_site(request)
    subject = 'Subscripción hecha ' + current_site.domain
    mail = create_mail(email, subject, 'mails/subscripcion.html', {
        'host': get_host_url(request),
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(email)),
        'cfg': Config.objects.first() if Config.objects.exists() else None
    })
    mail.send(fail_silently=False)
    messages.success(request,
                     f'Has sido subscrito a Fitness Army, le mantendremos informados de nuestras novedades.')
    return redirect(reverse('index'))


@method_decorator(csrf_exempt, require_GET)
def unsubscribe(request, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        sub = Subscriptor.objects.get(email=uid)
    except(TypeError, ValueError, OverflowError, Subscriptor.DoesNotExist):
        sub = None
    if sub is not None:
        sub.delete()
        messages.warning(request,
                         'Su subscripción ha sido cancelada! Puede volverse a subscribir si lo considera necesario.')
        return redirect(reverse('index'))
    else:
        messages.info(request, f'Usted no se encontraba subscrito en nuestra empresa.')
        return redirect(reverse('index'))


@api_view()
def product_list_api(request):
    product_list = Product.objects.filter(is_active=True)
    serializer = ProductSerializer(product_list, many=True)
    return Response(serializer.data, status=200)


def create_order(request: HttpRequest, **kwargs):
    # Datos del formulario
    name = request.POST.get('name')
    phone_number = request.POST.get('phone_number', None)
    email = request.POST.get('email')
    address = request.POST.get('address')
    # Calcular total
    cart = Cart(request)
    total = 0
    if cart.all():
        for c in cart.all():
            total += float(c['product']['price']) * float(c['quantity'])
        orden = Orden.objects.create(total=float(total), status='1', name=name, phone_number=phone_number,
                                     address=address, email=email)
        for c in cart.all():
            prod = Product.objects.get(pk=c['id'])
            ComponenteOrden.objects.create(orden=orden, producto=prod,
                                           respaldo=float(c['product']['price']) * float(c['quantity']),
                                           cantidad=int(c['quantity']))
            # Aki se rebaja
            prod.sales += int(c['quantity'])
            prod.save()
        request.session['last_order'] = str(orden.uuid)
        # Limpiar cart
        Cart(request).clear()
        return orden
    return None


def create_message_order(request: HttpRequest, orden: Orden):
    mensaje = 'Orden de compra:\n'
    mensaje += 'Ticket: ' + f'{str(orden.uuid)}\n'
    mensaje += 'Nombre: ' + orden.name + '\n'
    mensaje += 'Teléfono: ' + orden.phone_number + '\n'
    mensaje += '\nProductos comprados: \n'
    for c in orden.componente_orden.all():
        mensaje += str(c) + '\n'
    mensaje += 'Precio total: ' + '{:.2f}'.format(orden.total) + '\n'
    mensaje += '\nDatos de entrega:\n'
    mensaje += f'Dirección: {orden.address}.\n'
    return mensaje


def cancel_order(request, *args, **kwargs):
    orden = Orden.objects.get(pk=kwargs.get('pk'))
    orden.status = '3'
    orden.save()
    for c in orden.componente_orden.all():
        if c.producto:
            prod = c.producto
            prod.sales -= c.cantidad
            prod.save()
    return redirect('index')


def send_email_order(request, orden: Orden, mensaje: str):
    current_site = get_current_site(request)
    subject = 'Compra realizada ' + current_site.domain
    mail = create_mail(orden.email, subject, 'mails/orden.html', {
        'host': get_host_url(request),
        "domain": current_site.domain,
        # 'mensaje': mensaje.replace(" <br/> ", "\n"),
        'mensaje': mensaje.replace("\n", "<br>"),
        'cfg': Config.objects.first() if Config.objects.exists() else None
    })
    mail.send()
    print('Se envió un correo de orden')
