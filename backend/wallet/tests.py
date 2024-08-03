from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Wallet, Coin, WalletCoin, Transaction
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

class WalletAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            phone_number="09156974569",
            password="password123?S"
        )
        self.user2 = User.objects.create_user(
            phone_number="09339496512",
            password="password123?S"
        )

        self.wallet1 = Wallet.objects.create(owner=self.user1)
        self.wallet2 = Wallet.objects.create(owner=self.user2)
        
        self.coin , c = Coin.objects.get_or_create(symbol="BTC")

        self.wallet_coin1 = WalletCoin.objects.create(wallet=self.wallet1, coin=self.coin, balance=1)
        self.wallet_coin2 = WalletCoin.objects.create(wallet=self.wallet2, coin=self.coin, balance=0)
        self.access_token1 = str(AccessToken.for_user(self.user1))
        self.access_token2 = str(AccessToken.for_user(self.user2))
        
        self.wallet_url = reverse('api:v1:wallet:wallet-detail')
        self.coins_url = reverse('api:v1:wallet:coin-list')
        self.transfer_url = reverse('api:v1:wallet:transfer-coin')
        self.deposit_url = reverse('api:v1:wallet:deposit-coin')

    def test_wallet_detail_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token1}')
        response = self.client.get(self.wallet_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], str(self.user1))
        self.assertEqual(len(response.data['coins']), 1)

    def test_coin_list_view(self):
        response = self.client.get(self.coins_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['symbol'], "BTC")

    def test_transfer_coin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token1}')
        data = {
            "from_address": str(self.wallet1.address),
            "to_address": str(self.wallet2.address),
            "symbol": "BTC",
            "amount": 0.5
        }
        response = self.client.post(self.transfer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet_coin1.refresh_from_db()
        self.assertEqual(self.wallet_coin1.balance, 0.5)

        wallet_coin2 = WalletCoin.objects.get(wallet=self.wallet2, coin=self.coin)
        self.assertEqual(wallet_coin2.balance, 0.5)

    def test_deposit_coin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token2}')
        data = {
            "symbol": "BTC",
            "amount": 0.25
        }
        response = self.client.post(self.deposit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        wallet_coin2 = WalletCoin.objects.get(wallet=self.wallet2, coin=self.coin)
        self.assertEqual(wallet_coin2.balance, 0.25)

    def test_insufficient_balance_transfer(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token1}')
        data = {
            "from_address": str(self.wallet1.address),
            "to_address": str(self.wallet2.address),
            "symbol": "BTC",
            "amount": 2  
        }
        response = self.client.post(self.transfer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Not enough BTC in your wallet',response.data['non_field_errors'])

    def test_compare_balance_transfer(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token1}')
        data = {
            "from_address": str(self.wallet1.address),
            "to_address": str(self.wallet2.address),
            "symbol": "BTC",
            "amount": 0.3  
        }
        self.client.post(self.transfer_url, data, format='json')
        self.wallet_coin2 = WalletCoin.objects.get(id = self.wallet_coin2.id)
        self.wallet_coin1 = WalletCoin.objects.get(id = self.wallet_coin1.id)
        self.assertEqual(self.wallet_coin2.balance, 0.3)
        self.assertEqual(self.wallet_coin1.balance, 0.7)
