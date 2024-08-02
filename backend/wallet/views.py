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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
User = get_user_model()
class CustomPagination(PageNumberPagination):
    page_size = 100  
    page_size_query_param = 'page_size'

class WalletDetailView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        wallet , c= Wallet.objects.get_or_create(owner=self.request.user)
        return wallet

class CoinListView(generics.ListAPIView):
    queryset = Coin.objects.all().order_by('id')
    serializer_class = CoinSerializer
    pagination_class = CustomPagination

class TransferView(generics.GenericAPIView):

    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Transfer successful",
                examples={
                    "application/json": {
                        "detail": "Transfer successful."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "detail": "Insufficient balance."
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "detail": "User wallet does not exist."
                    }
                }
            ),
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'to_address': openapi.Schema(type=openapi.FORMAT_UUID),
                'amount': openapi.Schema(type=openapi.FORMAT_DECIMAL),
                'symbol': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['to_address','amount','symbol'],
        ),
    )
    def post(self, request, *args, **kwargs):
        source_wallet , c = Wallet.objects.get_or_create(owner=request.user)
        request.data['from_address'] = source_wallet.address
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipient_wallet = serializer.validated_data['recipient_wallet']
        coin = serializer.validated_data['coin']
        amount = serializer.validated_data['amount']
        wallet_coin , c = WalletCoin.objects.get_or_create(wallet=recipient_wallet , coin=coin)
        wallet_coin.balance += amount 
        wallet_coin.save()
        data = {'source_wallet' : source_wallet.id ,'recipient_wallet':recipient_wallet.id,'amount':amount,'transaction_type':'transfer'}
        transaction = TransactionSerializer(data=data)
        transaction.is_valid(raise_exception=True)
        transaction.save()
        return Response({"detail": _("Transfer successful.")}, status=status.HTTP_200_OK)

class DepositView(generics.GenericAPIView):
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        wallet , c = Wallet.objects.get_or_create(owner=request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        coin = serializer.validated_data['coin']
        amount = serializer.validated_data['amount']
        wallet_coin , c = WalletCoin.objects.get_or_create(wallet=wallet , coin=coin)
        wallet_coin.balance += amount
        wallet_coin.save()
        data={'recipient_wallet':wallet.id,'amount':amount,'transaction_type':'deposit'}
        transaction = TransactionSerializer(data=data)
        transaction.is_valid(raise_exception=True)
        transaction.save()
        return Response({"detail": _("Deposit successful.")}, status=status.HTTP_200_OK)

