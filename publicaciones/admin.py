from django.contrib import admin

from publicaciones.models import Publicacion, Adopcion, CampaniaDonacion, Donacion, Tarjeta

# Register your models here.
admin.site.register(Publicacion)
admin.site.register(Adopcion)
admin.site.register(CampaniaDonacion)
admin.site.register(Donacion)
admin.site.register(Tarjeta)

