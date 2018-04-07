from django.contrib import admin

from app.nominas.models import Cargo


class CargoAdmin(admin.ModelAdmin):
    search_fields = ('nombre', )
    list_display = ('nombre', 'descripcion',)
    list_display_links = ('nombre',)
    list_per_page = 25


admin.site.register(Cargo, CargoAdmin)

