from rest_framework import serializers
from ..models import Warehouse

class WarehouseSerializer(serializers.Serializer):
    class Meta:
        model = Warehouse
        fields = ['code', 'name', 'address', 'city', 'created_at', 'update_at']
    
    def validate(self, value):
        if ' ' in value:
            raise serializers.Serializer.ValidationError('code no debe contener espacios')
        return value