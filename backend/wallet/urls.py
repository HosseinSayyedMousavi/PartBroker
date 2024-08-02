from django.urls import path
from .views import WalletDetailView , CoinListView , TransferView , DepositView

urlpatterns = [
    path('wallet/', WalletDetailView.as_view(), name='wallet-detail'),
    path('coins/', CoinListView.as_view(), name='coin-list'),
    path('transfer/', TransferView.as_view(), name='transfer-coin'),
    path('deposit/', DepositView.as_view(), name='deposit-coin')
]