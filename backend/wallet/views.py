# Create your views here.
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions
from .models import Wallet , Coin , WalletCoin
from .serializers import WalletSerializer , CoinSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import TransferSerializer , DepositSerializer , TransactionSerializer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
User = get_user_model()
class CustomPagination(PageNumberPagination):
    page_size = 100  
    page_size_query_param = 'page_size'

class WalletDetailView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        wallet , _= Wallet.objects.get_or_create(owner=self.request.user)
        return wallet

class CoinListView(generics.ListAPIView):
    queryset = Coin.objects.all().order_by('id')
    serializer_class = CoinSerializer
    pagination_class = CustomPagination

class TransferView(generics.GenericAPIView):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        source_wallet , _ = Wallet.objects.get_or_create(owner=request.user)
        request.data['from_address'] = source_wallet.address
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipient_wallet = serializer.validated_data['recipient_wallet']
        coin = serializer.validated_data['coin']
        amount = serializer.validated_data['amount']
        wallet_coin , _ = WalletCoin.objects.get_or_create(wallet=recipient_wallet , coin=coin)
        wallet_coin.balance += amount 
        wallet_coin.save()
        transaction = TransactionSerializer(source_wallet = source_wallet ,recipient_wallet=recipient_wallet,amount=amount,transaction_type='transfer')
        transaction.is_valid(raise_exception=True)
        transaction.save()
        return Response({"detail": _("Transfer successful.")}, status=status.HTTP_200_OK)

class DepositView(generics.GenericAPIView):
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        wallet , _ = Wallet.objects.get_or_create(owner=request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        coin = serializer.validated_data['coin']
        amount = serializer.validated_data['amount']
        wallet_coin , _ = WalletCoin.objects.get_or_create(wallet=wallet , coin=coin)
        wallet_coin.balance += amount
        wallet_coin.save()
        transaction = TransactionSerializer(recipient_wallet=wallet,amount=amount,transaction_type='deposit')
        transaction.is_valid(raise_exception=True)
        transaction.save()
        return Response({"detail": _("Deposit successful.")}, status=status.HTTP_200_OK)

