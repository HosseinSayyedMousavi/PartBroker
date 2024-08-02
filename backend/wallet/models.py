from django.db import models
import uuid
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Coin(models.Model):

    symbol = models.CharField(max_length=20,unique=True)
    price = models.FloatField(default=0)
    def __str__(self):
        return self.symbol


class Wallet(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Wallet of {self.owner}"


class WalletCoin(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='wallet_coin')
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='wallet_coin')
    balance = models.FloatField(default=0,validators=[MinValueValidator(0.0)])
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ["wallet", "coin"]

    def __str__(self):
        return f"{self.coin} balance in wallet of {self.wallet.owner}"