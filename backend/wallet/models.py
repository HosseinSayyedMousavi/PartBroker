from django.db import models
import uuid
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

User = get_user_model()
# Create your models here.
class Coin(models.Model):
    symbol = models.CharField(max_length=20,unique=True)
    price = models.FloatField(default=0,validators=[MinValueValidator(0)])
    def __str__(self):
        return self.symbol


class Wallet(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(_(f"Wallet of {self.owner}"))


class WalletCoin(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='wallet_coin')
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='wallet_coin')
    balance = models.DecimalField(max_digits=20,decimal_places=12,default=Decimal('0'), validators=[MinValueValidator(Decimal('0'))])
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ["wallet", "coin"]

    def __str__(self):
        return str(_(f"{self.coin} balance in wallet of {self.wallet.owner}"))


class Transaction(models.Model):
    source_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True , blank = True ,related_name='transaction_source_wallet')
    recipient_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE,related_name='transaction_recipient_wallet')
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20,decimal_places=12, validators=[MinValueValidator(Decimal('0.00000000001'))])
    transaction_type = models.CharField(choices = [('deposit','deposit'),('transfer','transfer')])
    date = models.DateTimeField(auto_now_add=True)


