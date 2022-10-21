import requests
from datetime import datetime


def openInterest(symbol):
    time_now = datetime.now().timestamp()
    endTime = int((time_now//60)*60 * 1000)
    startTime = int(((time_now//60)*60 - 60*13*60) * 1000)
    interval = "m1"
    url = f'https://fapi.coinglass.com/api/openInterest/kline2?exName=Binance&interval={interval}&endTime={endTime}&startTime={startTime}&pair={symbol}USDT&rateType=f&type=1'
    params = {}
    response = requests.request("GET", url, data = params)
    Data = response.json()['data']
    m5 = ((endTime // 1000) - 5*60) * 1000
    m15 = ((endTime // 1000) - 15*60) * 1000
    H1 = ((endTime // 1000) - 60*60) * 1000
    H4 = ((endTime // 1000) - 4*3600) * 1000
    openInterest_history = {}
    for data in Data[:]:
        if data['t'] == m5:
            openInterest_history["m5"] = data['c']
        elif data['t'] == m15:
            openInterest_history["m15"] = data['c']
        elif data['t'] == H1:
            openInterest_history["H1"] = data['c']
        elif data['t'] == H4:
            openInterest_history["H4"] = data['c']

    openInterest_now = Data[-1]['c']
    openInterest_history["m5"] = round((openInterest_now - openInterest_history["m5"])/abs(openInterest_history["m5"]) * 100, 2)
    openInterest_history["m15"] = round((openInterest_now - openInterest_history["m15"])/abs(openInterest_history["m15"]) * 100, 2)
    openInterest_history["H1"] = round((openInterest_now - openInterest_history["H1"])/abs(openInterest_history["H1"]) * 100, 2)
    openInterest_history["H4"] = round((openInterest_now - openInterest_history["H4"])/abs(openInterest_history["H4"]) * 100, 2)
    return openInterest_now, openInterest_history


openInterest(symbol = 'APT')





