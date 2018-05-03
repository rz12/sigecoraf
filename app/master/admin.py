from django.contrib import admin

from app.master.models import Empresa, Item, Catalogo


class EmpresaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'descripcion')
    list_display = ('nombre', 'descripcion',)
    list_display_links = ('nombre',)
    list_per_page = 25


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1


class CatalogoAdmin(admin.ModelAdmin):
    search_fields = ('codigo',)
    list_display = ('codigo', 'nombre',)
    list_display_links = ('codigo',)
    inlines = [ItemInline]
    list_per_page = 25


admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Catalogo, CatalogoAdmin)
