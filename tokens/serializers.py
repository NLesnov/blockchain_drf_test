from rest_framework import serializers
from .models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
        read_only_fields = ('unique_hash', 'tx_hash')


class TotalSupplySerializer(serializers.Serializer):
    total_supply = serializers.IntegerField()
