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
    }


class IndexView(generic.TemplateView):
    template_name = 'pages/start_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Fitness Army | Inicio'
        context['current_url'] = reverse_lazy('index')
        context['inicio'] = True
        context.update(get_global_context(self.request))
        return context
