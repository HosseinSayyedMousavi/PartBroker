from rest_framework import serializers
from .models import Wallet, WalletCoin , Coin , Transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
class WalletCoinSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(source='coin.symbol', read_only=True)
    price = serializers.FloatField(source='coin.price', read_only=True)

    class Meta:
        model = WalletCoin
        fields = ['symbol', 'price', 'balance', 'updated_date']

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = "__all__"

class WalletSerializer(serializers.ModelSerializer):
    coins = WalletCoinSerializer(source='wallet_coin', many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    total_value = serializers.SerializerMethodField()
    class Meta:
        model = Wallet
        fields = ['owner', 'address', 'created_date', 'updated_date', 'coins','total_value']
    
    def get_total_value(self,obj):
        total = 0
        wallet_coins = obj.wallet_coin.all() .order_by('id')
        for wallet_coin in wallet_coins:
            total += wallet_coin.coin.price * wallet_coin.balance
        return total

class TransferSerializer(serializers.Serializer):
    from_address = serializers.UUIDField()
    to_address = serializers.UUIDField()
    symbol = serializers.CharField()
    amount = serializers.FloatField(min_value=0.00000000001)
    def validate(self, attrs):                                     
        valid = super().validate(attrs)
        source_wallet = get_object_or_404(Wallet,address=valid['from_address'])        
        recipient_wallet = get_object_or_404(Wallet,address=valid['to_address'])
        coin = get_object_or_404(Coin , symbol=valid['symbol'])
        wallet_coin = WalletCoin.objects.filter(wallet=source_wallet , coin=coin , balance__gte=valid['amount'])
        if not wallet_coin.exists() : raise serializers.ValidationError(_(f"Not enough {coin.symbol} in your wallet"))
        valid['recipient_wallet'] = recipient_wallet
        valid['coin'] = coin
        return valid

class DepositSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    amount = serializers.FloatField(min_value=0.00000000001)

    def validate(self, attrs):
        valid = super().validate(attrs)
        coin =get_object_or_404(Coin , symbol=valid['symbol'])
        valid['coin'] = coin
        return valid

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
