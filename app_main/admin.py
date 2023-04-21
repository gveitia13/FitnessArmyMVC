from django.contrib import admin
from django.contrib.auth.models import User, Group
from solo.admin import SingletonModelAdmin

from app_main.forms import ConfigForm, ProductForm, PropertyForm
from app_main.models import Config, Property, Product


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


# admin.site.unregister(User)
admin.site.unregister(Group)
