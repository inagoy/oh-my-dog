from django.contrib import admin

from publicaciones.models import Publicacion, Adopcion, CampaniaDonacion, Donacion, Tarjeta, Postulante, PerdidoEncontrado

# Register your models here.
admin.site.register(Publicacion)
admin.site.register(Adopcion)
admin.site.register(CampaniaDonacion)
admin.site.register(Donacion)
admin.site.register(Tarjeta)
admin.site.register(Postulante)
admin.site.register(PerdidoEncontrado)
