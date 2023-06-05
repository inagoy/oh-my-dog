from django.contrib import admin

from publicaciones.models import Publicacion, Adopcion, CampaniaDonacion

# Register your models here.
admin.site.register(Publicacion)
admin.site.register(Adopcion)
admin.site.register(CampaniaDonacion)

