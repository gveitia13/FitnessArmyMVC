from django.contrib import admin, messages
from django.contrib.auth.models import User, Group
from solo.admin import SingletonModelAdmin

from app_main.forms import ConfigForm, ProductForm, PropertyForm
from app_main.models import Config, Property, Product, Contact


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
        'name', 'img_link', 'price', 'is_active', 'is_important')
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


# admin.site.unregister(User)
admin.site.unregister(Group)
