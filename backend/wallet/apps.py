from django.apps import AppConfig
from django.conf import settings
import json
BASE_DIR=settings.BASE_DIR
coin_path = BASE_DIR / "wallet/coins.json"

class WalletConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wallet"
    def ready(self):
        from .models import Coin
        with open(coin_path,"r") as f:
            symbols = json.loads(f.read())
            for symbol in symbols :
                Coin.objects.get_or_create(symbol=symbol)