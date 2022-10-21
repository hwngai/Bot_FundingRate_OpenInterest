import requests
from datetime import datetime

def fundingRateHistory(symbol):
    time_now = datetime.now().timestamp()
    endTime = int((time_now//60)*60 * 1000)
    startTime = int(((time_now//60)*60 - 60*13*60) * 1000)
    interval = "m1"
    url = f'https://fapi.coinglass.com/api/fundingRate/kline2?exName=&interval={interval}&endTime={endTime}&startTime={startTime}&pair=&symbol={symbol}'
    params = {}
    response = requests.request("GET", url, data = params)
    Data = response.json()['data']
    m5 = ((endTime // 1000) - 5*60) * 1000
    m15 = ((endTime // 1000) - 15*60) * 1000
    H1 = ((endTime // 1000) - 60*60) * 1000
    H4 = ((endTime // 1000) - 4*3600) * 1000
    fundingRate_history = {}
    for data in Data[:]:
        if data['t'] == m5:
            fundingRate_history["m5"] = data['c']
        elif data['t'] == m15:
            fundingRate_history["m15"] = data['c']
        elif data['t'] == H1:
            fundingRate_history["H1"] = data['c']
        elif data['t'] == H4:
            fundingRate_history["H4"] = data['c']

    url_symbol = 'https://fapi.coinglass.com/api/fundingRate/v2/home'
    resp = requests.get(url_symbol)
    data = resp.json()
    for coin in data['data']:
        if coin["symbol"] == symbol:
            markets = coin["uMarginList"]
            for market in markets:
                if market["exchangeName"] == "Binance":
                    if "rate" in market:
                        rate = market["rate"]
    fundingRate_history["m5"] = round((rate - fundingRate_history["m5"])/abs(fundingRate_history["m5"]) * 100, 2)
    fundingRate_history["m15"] = round((rate - fundingRate_history["m15"])/abs(fundingRate_history["m15"]) * 100, 2)
    fundingRate_history["H1"] = round((rate - fundingRate_history["H1"])/abs(fundingRate_history["H1"]) * 100, 2)
    fundingRate_history["H4"] = round((rate - fundingRate_history["H4"])/abs(fundingRate_history["H4"]) * 100, 2)
    return rate, fundingRate_history
