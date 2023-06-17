from import_export import resources, fields, widgets
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from alarms.models import AlarmaEvent,AlarmaVecinal,Miembro,Vivienda
   



class AlarmaEventR(resources.ModelResource):
    
    miembro = Field(
        column_name='miembro',
        attribute='miembro',
        widget=ForeignKeyWidget(model=Miembro, field='id'))
    
    
    class Meta:
        model = AlarmaEvent
        
            
        
        
class AlarmaVecinalR(resources.ModelResource): 
    
    class Meta:
        model = AlarmaVecinal
        
        

class MiembroR(resources.ModelResource): 
    
    vivienda = Field(
        column_name='vivienda',
        attribute='vivienda',
        widget=ForeignKeyWidget(model=Vivienda, field='id'))
    
    
    class Meta:
        model = Miembro
        
class ViviendaR(resources.ModelResource):

    alarma_vecinal = Field(
        column_name='alarma_vecinal',
        attribute='alarma_vecinal',
        widget=ForeignKeyWidget(model=AlarmaVecinal, field='id'))
    
    
    class Meta:
        model = Vivienda
    
        