

from rest_framework import serializers
from .models import Tramite, Derecho


class DerechoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Derecho
        fields = '__all__'


class TramiteSerializer(serializers.ModelSerializer):
    derechos = DerechoSerializer(many=True)

    class Meta:
        model = Tramite
        fields = '__all__'
