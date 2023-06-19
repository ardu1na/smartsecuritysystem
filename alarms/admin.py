from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from alarms.resources import AlarmaEventR, AlarmaVecinalR, MiembroR, ViviendaR
from alarms.models import *

class UsuariosInline(admin.StackedInline):
    model = Miembro
    extra  = 0
    
    
class AlarmaInline(admin.StackedInline):
    model = AlarmaEvent    
    extra  = 0

class ViviendaInline(admin.StackedInline):
    model = Vivienda    
    extra  = 0
    
    
    
    

    
class BarrioAdmin(ImportExportModelAdmin):
    inlines =  [ViviendaInline,]
    resource_class = AlarmaVecinalR

admin.site.register(AlarmaVecinal, BarrioAdmin)



class ViviendaAdmin(ImportExportModelAdmin):
    resource_class = ViviendaR
    list_display = [ 'get_direccion_con_municipio_y_provincia', 'alarma_vecinal', 'get_miembros_string']
    inlines =  [UsuariosInline,]
admin.site.register(Vivienda, ViviendaAdmin)



class UsuarioAdmin(ImportExportModelAdmin):
    resource_class = MiembroR
    list_display = [ 'get_nombre_completo', 'pk', 'get_edad', 'get_barrio', 'vivienda']
    inlines =  [AlarmaInline,]
admin.site.register(Miembro, UsuarioAdmin)



class AlarmAdmin(ImportExportModelAdmin):
    resource_class = AlarmaEventR
admin.site.register(AlarmaEvent, AlarmAdmin)



admin.site.register(Municipio)
admin.site.register(Provincia)
admin.site.register(Pais)