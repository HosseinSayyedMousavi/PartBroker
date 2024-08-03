from django.conf import settings
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import json
import sys
BASE_DIR=settings.BASE_DIR
coin_path = BASE_DIR / "wallet/coins.json"

class WalletConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wallet"
    def ready(self):
        @receiver(post_migrate)
        def load_coin_symbols(sender, **kwargs):
            if 'test' in sys.argv:
                return 
            if sender.name == 'wallet': 
                from .models import Coin
                with open(coin_path, "r") as f:
                    symbols = json.loads(f.read())
                    for symbol in symbols:
                        Coin.objects.get_or_create(symbol=symbol)