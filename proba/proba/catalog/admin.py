# superuser_1: mooty {{  jSdmD_sj67 // http://127.0.0.1:8000/admin
# superuser_2: miitu {{ sdjvkjd_324 // miitu@example.com // dni:43


""" EXPLICACIÓN DE ESTE FICHERO "admin.py":


"""

from django.contrib import admin
from .models import Usuario, Torneo, Videojuego, Partida, Participacion, Resultado

# No necesito registrar Usuario, ya que es una clase abstracta
# admin.site.register(Usuario)
""" Explicación:
- list_display: Define las columnas que se mostrarán en la lista de 
                objetos (el panel de administración de Django).
- list_filter: Añade opciones de filtrado en la barra lateral del panel de administración 
                para facilitar la búsqueda de objetos basados en ciertos campos.
- search_fields: Habilita la funcionalidad de búsqueda en el panel de administración
                para ciertos campos específicos.
"""

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('alias', 'nombre', 'email', 'dni')  # Personaliza las columnas visibles
    search_fields = ('alias', 'nombre', 'email')  # Agrega búsqueda por campos específicos

@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'videojuego', 'fecha_inicio', 'estado')
    list_filter = ('videojuego', 'estado')  # Filtros en el panel
    search_fields = ('nombre',)

@admin.register(Videojuego)
class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'videojuego', 'fecha_hora', 'torneo')
    list_filter = ('videojuego', 'torneo')  # Filtros por videojuego y torneo

@admin.register(Participacion)
class ParticipacionAdmin(admin.ModelAdmin):
    list_display = ('partida', 'jugador', 'puntaje', 'resultado', 'tiempo_jugado')
    search_fields = ('jugador__alias', 'partida__nombre')

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ("participacion", "descripcion", "puntaje", "otras_estadisticas")
    search_fields = ('puntaje', 'participacion__partida')
