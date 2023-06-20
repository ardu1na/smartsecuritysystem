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
    inlines = [ViviendaInline,]
    exclude = ['deleted_at', 'state']
    
    def get_export_resource_class(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get_export_resource_class(request, *args, **kwargs)
        else:
            return None
    
    def get_import_resource_class(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get_import_resource_class(request, *args, **kwargs)
        else:
            return None

admin.site.register(AlarmaVecinal, BarrioAdmin)


class ViviendaAdmin(ImportExportModelAdmin):
    resource_class = ViviendaR
    list_display = [ 'alarma_vecinal', 'get_miembros_string']
    inlines =  [UsuariosInline,]
    exclude = ['deleted_at', 'state']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # solo edita y ve su vivienda
        if not request.user.is_superuser:
            try:
                miembro = request.user.miembro
                vivienda = miembro.vivienda
                queryset = queryset.filter(id=vivienda.id)
            except Miembro.DoesNotExist:
                queryset = queryset.none()
        
        return queryset

    
    
admin.site.register(Vivienda, ViviendaAdmin)



class UsuarioAdmin(ImportExportModelAdmin):
    resource_class = MiembroR
    list_display = [ 'get_nombre_completo', 'pk', 'get_edad', 'get_barrio', 'vivienda']
    inlines =  [AlarmaInline,]
    exclude = ['deleted_at', 'state']

    def get_queryset(self, request): # obtieniendo su propio perfil
        queryset = super().get_queryset(request)
        
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        
        return queryset
    
    
admin.site.register(Miembro, UsuarioAdmin)

class AlarmAdmin(ImportExportModelAdmin):
    resource_class = AlarmaEventR
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        if not request.user.is_superuser:
            try:
                miembro = request.user.miembro
                queryset = queryset.filter(
                    miembro__vivienda__alarma_vecinal=miembro.vivienda.alarma_vecinal
                    ) # obteniendo los eventos de alarma de su vecindad
            except Miembro.DoesNotExist:
                queryset = queryset.none()
        
        return queryset
    
admin.site.register(AlarmaEvent, AlarmAdmin)


admin.site.register(Municipio)
admin.site.register(Provincia)
admin.site.register(Pais)