from rest_framework import serializers
from ..models import Crypto

class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = ('name', 'slug', 'price', 'last_24h', 'last_7d', 'date')
        read_only_fields = ('slug', 'price', 'last_24h', 'last_7d', 'date')

class ConvertCryptoSerializer(serializers.Serializer):
    fromCoin = serializers.CharField(trim_whitespace=True)
    toCoin = serializers.CharField(trim_whitespace=True)
    amount = serializers.FloatField(min_value=0)