from celery import shared_task
from .models import Coin
import requests
from tqdm import tqdm

@shared_task
def update_coins():
    url = "https://api.fzassistant.com/api/v1/coin_price/"
    coins = Coin.objects.all().order_by('id')
    symbols = coins.values_list('symbol', flat=True)
    params = {"symbols":  ','.join(symbols)}
    response = requests.get(url,params=params).json()
    for resp in tqdm(response):
        Coin.objects.filter(symbol=resp['symbol_coin']).update(price=resp['price'])


