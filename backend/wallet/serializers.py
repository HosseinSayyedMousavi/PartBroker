from rest_framework import serializers
from .models import Wallet, WalletCoin , Coin

class WalletCoinSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source='coin.symbol', read_only=True)
    price = serializers.FloatField(source='coin.price', read_only=True)

    class Meta:
        model = WalletCoin
        fields = ['symbol', 'price', 'balance', 'updated_date']

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['id', 'symbol', 'price']

class WalletSerializer(serializers.ModelSerializer):
    coins = WalletCoinSerializer(source='wallet_coins', many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Wallet
        fields = ['owner', 'address', 'created_date', 'updated_date', 'coins']
