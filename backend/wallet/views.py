from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination

# Create your views here.
from rest_framework import generics, permissions
from .models import Wallet , Coin
from .serializers import WalletSerializer , CoinSerializer

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

