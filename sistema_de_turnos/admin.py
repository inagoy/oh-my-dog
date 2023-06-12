from django.contrib import admin
from .models import Turno, Atencion, Inyeccion, Desparasitante

admin.site.register(Turno)
admin.site.register(Atencion)
admin.site.register(Inyeccion)
admin.site.register(Desparasitante)
