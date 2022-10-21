import requests
def price(symbol):
    r_spot = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT')
    r_futures = requests.get(f'https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}USDT')
    print(r_spot.json(), r_futures.json())
    price_spot = float(r_spot.json()['price'])
    price_futures = float(r_futures.json()['price'])
    ratio = round(100*abs(price_spot - price_futures) / min(price_futures, price_spot),4)
    return price_spot, price_futures,ratio