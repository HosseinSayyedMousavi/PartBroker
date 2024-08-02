from django.urls import path
from .views import WalletDetailView , CoinListView , TransferSerializer

urlpatterns = [
    path('api/wallet/', WalletDetailView.as_view(), name='wallet-detail'),
    path('api/coins/', CoinListView.as_view(), name='coin-list'),
    path('api/transfer/', TransferSerializer.as_view(), name='transfer-coin'),
]