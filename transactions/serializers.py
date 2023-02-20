

from rest_framework import serializers
from .models import Tramite,Derecho, Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
class DerechoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Derecho
        fields = '__all__'

class TramiteSerializer(serializers.ModelSerializer):
    derechos = DerechoSerializer(many=True)
    class Meta:
        model = Tramite
        fields = '__all__'

    def create(self, validated_data):
        derecho_data = validated_data.pop('derechos')
        derechos = [Derecho.objects.get(pk=derecho['id']) for derecho in derecho_data]
        tramite = Tramite.objects.create(**validated_data)
        tramite.derecho.set(derechos)
        return tramite