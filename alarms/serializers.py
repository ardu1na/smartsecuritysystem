from rest_framework import serializers
from alarms.models import AlarmaEvent


class AlarmaEventSerializer(serializers.ModelSerializer):
    miembro = serializers.StringRelatedField()
    vivienda = serializers.StringRelatedField(source='miembro.vivienda')
    wp = serializers.CharField(source='miembro.get_wp')

    class Meta:
        model = AlarmaEvent
        fields = ['miembro', 'tipo', 'datetime', 'vivienda', 'wp']
        extra_kwargs = {
            'datetime': {'format': '%Y-%m-%d %H:%M:%S'}
        }
        
    