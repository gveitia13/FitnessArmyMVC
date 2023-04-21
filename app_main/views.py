from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.views import generic

from FitnessArmyMVC.utils import get_host_url
from app_main.models import Config, Product


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
        context['inicio'] = True
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
        context['inicio'] = True
        context['high_price'] = Product.objects.filter(is_active=True).order_by('price')[0].price
        return context
