from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.views import generic

from FitnessArmyMVC.utils import get_host_url
from app_main.models import Config, Product, Contact


def get_global_context(request):
    current_site = get_current_site(request)
    return {
        'cfg': Config.objects.first() if Config.objects.exists() else None,
        'product_list': Product.objects.filter(is_active=True),
        'host': get_host_url(request),
        "domain": current_site.domain,
        'promo_list': [i for i in range(7)]
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

# @method_decorator(csrf_exempt, require_POST)
# def create_contact(request):
#     try:
#         contact = Contact.objects.create(email=request.POST['email'], subject=request.POST['subject'],
#                                          name=request.POST['name'], message=request.POST['message'])
#         print(contact)
#         current_site = get_current_site(request)
#         mail = create_mail(contact.email, 'Contacto realizado', 'core/mails/contact_mail.html', {
#             'host': get_host_url(request),
#             "domain": current_site.domain,
#             'name': request.POST['name'],
#             'cfg': Config.objects.first() if Config.objects.exists() else None
#         })
#         mail.send()
#         messages.success(request,
#                          'Se ha enviado una notificación por correo, un administrador se pondrá en contacto con usted.')
#         if Config.objects.exists():
#             send_mail('Nuevo contacto',
#                       f'Correo: {contact.email}\nAsunto: {contact.subject}\nNombre: {contact.name}\nMensaje: {contact.message}',
#                       settings.EMAIL_HOST_USER, [Config.objects.first().email])
#     except Exception as e:
#         print(str(e))
#         messages.error(request, 'Ha ocurrido un error en el servidor! Intente de nuevo.')
#     return redirect(reverse('index'))
