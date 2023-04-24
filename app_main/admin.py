import threading

from django.contrib import admin, messages
from django.contrib.auth.models import User, Group
from solo.admin import SingletonModelAdmin

from app_main.forms import ConfigForm, ProductForm, PropertyForm
from app_main.models import Config, Property, Product, Contact, Subscriptor, ComponenteOrden, Orden, Offer


@admin.register(Config)
class ConfigAdmin(SingletonModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'address')
    fieldsets = [
        ('Datos principales',
         {'fields': ('name', 'email', 'address', 'phone_number',)}),
        ('Redes sociales',
         {'fields': ('instagram', 'facebook', 'twitter', 'whatsapp',)}),
        ('Fotos', {'fields': ('logo', 'get_logo', 'icon', 'banner',)})
    ]

    form = ConfigForm
    readonly_fields = ['get_logo']


class PropertyInline(admin.TabularInline):
    fields = ('text',)
    extra = 3
    model = Property
    form = PropertyForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'img_link', 'price', 'sales', 'is_active', 'is_important')
    fieldsets = [
        ('Datos Principales:', {
            'fields': ('name', 'price', 'is_active', 'is_important')
        }),
        ('Descripción:', {
            'fields': ('image', 'img_link', 'info',)
        })
    ]
    search_fields = ('name',)
    list_per_page = 10
    actions = ['Desactivar_productos', 'Activar_productos']
    readonly_fields = ('img_link',)
    inlines = (PropertyInline,)
    form = ProductForm

    def Desactivar_productos(self, request, queryset):
        for p in queryset:
            p.is_active = False
            p.save()

    def Activar_productos(self, request, queryset):
        for p in queryset:
            p.is_active = True
            p.save()


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'is_attended')
    list_display_links = ('name',)
    list_editable = ('is_attended',)
    list_per_page = 20
    fields = ('is_attended', 'name', 'email', 'phone_number', 'message')
    readonly_fields = ('name', 'email', 'message', 'phone_number')
    actions = ['Marcar_como_atendido', 'Marcar_como_desatendido']

    def Marcar_como_atendido(self, request, queryset):
        cnt = queryset.filter(is_attended=False).update(is_attended=True)
        self.message_user(request, '{} Contactos marcados como atendidos.'.format(cnt), messages.SUCCESS)

    def Marcar_como_desatendido(self, request, queryset):
        cnt = queryset.filter(is_attended=True).update(is_attended=False)
        self.message_user(request, '{} Contactos marcados como desatendidos.'.format(cnt), messages.WARNING)

    def has_add_permission(self, request):
        return False


@admin.register(Subscriptor)
class SubscriptorAdmin(admin.ModelAdmin):
    list_display = ('email',)
    list_per_page = 20
    fields = ('email',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ComponenteOrdenInline(admin.StackedInline):
    model = ComponenteOrden
    extra = 0


class OrdenAdmin(admin.ModelAdmin):
    list_display = ('get_status', 'uuid', 'date_created', 'get_componente', 'get_total', 'email',)
    list_display_links = ('get_status', 'uuid')
    list_filter = ('status',)
    search_fields = ('uuid',)
    actions = ['Cancelar_Orden']
    list_per_page = 10
    # inlines = [ComponenteOrdenInline]
    readonly_fields = ['get_status', 'get_componente', 'total', 'name', 'email', 'phone_number', 'address', ]
    exclude = ['link_de_pago', 'status']

    def Cancelar_Orden(self, request, queryset):
        for o in queryset:
            if o.status != '3':
                o.status = '3'
                o.save()
                for c in o.componente_orden.all():
                    if c.producto:
                        prod = c.producto
                        prod.sales -= c.cantidad
                        prod.save()


class ComponenteOrdenAdmin(admin.ModelAdmin):
    list_display = ('orden', 'Componente')
    list_filter = ('producto',)
    search_fields = ('orden', 'producto')
    list_per_page = 20

    def has_change_permission(self, request, obj=None):
        return False


def async_send_offer_mail(queryset):
    for i in queryset:
        i.send_offer_mail()


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('get_status', 'subject', 'message', 'date_created')
    exclude = ['date_created', 'status']
    readonly_fields = ['get_status']
    actions = ['Enviar_Ofertas']

    def Enviar_Ofertas(self, request, queryset):
        thread = threading.Thread(target=async_send_offer_mail, args=(queryset,))
        thread.start()
        for i in queryset:
            i.status = '1'
            i.save()
        self.message_user(request, '{} Ofertas enviadas.'.format(queryset.count()), messages.SUCCESS)


admin.site.register(Orden, OrdenAdmin)
admin.site.register(ComponenteOrden, ComponenteOrdenAdmin)
# admin.site.unregister(User)
admin.site.unregister(Group)
