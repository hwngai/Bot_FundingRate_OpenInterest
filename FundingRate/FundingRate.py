from telegram_message_sender import send_message
import requests as req
import threading
import time

history_fundingRate = {}
fundingRateValue = 0.1
listPercentChangeRate = {}
listSubscribe = [{"symbol": "BTC","calculation":">", "value": "0.01"}, {"symbol": "ETH","calculation":">", "value": "0.01"}]
biananceCoins = {}

def removeSymbol(symbol, calculation):
    for coin in listSubscribe:
        if coin['symbol'].lower() == symbol.lower() and coin['calculation'] == calculation:
            listSubscribe.remove(coin)


def pushMarketFundingRate(TIME, listSubscribe, c = 0):
    global history_fundingRate
    if c == 0 :
        threading.Timer(TIME, pushMarketFundingRate, (TIME, listSubscribe)).start()
        time.sleep(1)
    url = 'https://fapi.coinglass.com/api/fundingRate/v2/home'
    resp = req.get(url)
    data = resp.json()
    teleContent = ""
    selectedSymbols = []
    allcoin = 0
    listNotifi=[]
    for coin in data['data']:
        markets = coin["uMarginList"]
        for market in markets:
            if market["exchangeName"] == "Binance":
                if "rate" in market:
                    rate = market["rate"]
                    biananceCoins_rate = biananceCoins[coin["symbol"]][0]
                    try:
                        percent_rate = (rate - biananceCoins_rate)/abs(biananceCoins_rate) * 100
                        #percent_openinterest = (openinterest - biananceCoins_openinterest)/abs(biananceCoins_openinterest) * 100
                        #biananceCoins_openinterest = biananceCoins[coin["symbol"]][1]
                        #percentChangeRate_openinterest = "{0:.0f}%".format(0)
                    except:
                        percent_rate = 0

                    percentChangeRate_openinterest = 0
                    content = f"Coin:*{coin['symbol']}* {str(rate)}/*{str(round(percent_rate, 2))}%*"
                    if len(listSubscribe) > 0:
                        for subscribe in listSubscribe:
                            if subscribe["symbol"].lower() == coin["symbol"].lower() or subscribe["symbol"].lower() == "allcoin":
                                if subscribe["symbol"].lower() == "allcoin":
                                    allcoin = 1
                                if subscribe["calculation"] == "<":
                                    if (float(rate) < float(subscribe["value"])) and coin["symbol"] not in selectedSymbols:
                                        teleContent = teleContent + content + "\n"
                                        listNotifi.append((content, abs(float(rate))))
                                        selectedSymbols.append(coin["symbol"])
                                        history_fundingRate[coin['symbol']] = float(rate)
                                        removeSymbol(coin["symbol"], "<")
                                elif subscribe["calculation"] == ">":
                                    if (float(rate) > float(subscribe["value"])) and coin["symbol"] not in selectedSymbols:
                                        teleContent = teleContent + content + "\n"
                                        listNotifi.append((content, abs(float(rate))))
                                        selectedSymbols.append(coin["symbol"])
                                        history_fundingRate[coin['symbol']] = float(rate)
                                        removeSymbol(coin["symbol"], ">")

    if allcoin == 1:
        try:
            removeSymbol("allCoin", "<")
            removeSymbol("allcoin", "<")
        except:
            removeSymbol("allCoin", ">")
            removeSymbol("allcoin", ">")

    history_fundingRate = {k: v for k, v in sorted(history_fundingRate.items(), key=lambda item: item[1])}
    listNotifi = sorted(listNotifi, key=lambda val: val[1], reverse=True)
    teleContent=""
    for notifi in listNotifi:
        teleContent = teleContent + notifi[0] + "\n"
    send_message(teleContent)


def mutationsFundingRate(ratio = 100):
    threading.Timer(10.0, mutationsFundingRate).start()
    url = 'https://fapi.coinglass.com/api/fundingRate/v2/home'
    resp = req.get(url)
    data = resp.json()
    teleContent = ""
    for coin in data['data']:
        markets = coin["uMarginList"]
        for market in markets:
            if market["exchangeName"] == "Binance":
                if "rate" in market:
                    rate = market["rate"]
                    #openinterest = openInterest(coin["symbol"])
                    try:
                        biananceCoins_rate = biananceCoins[coin["symbol"]][0]
                        #biananceCoins_openinterest = biananceCoins[coin["symbol"]][1]

                        percent_rate = (rate - biananceCoins_rate)/abs(biananceCoins_rate) * 100

                        #percent_openinterest = (openinterest - biananceCoins_openinterest)/abs(biananceCoins_openinterest) * 100

                        percentChangeRate_openinterest = 0

                        if abs(float(percent_rate)) > ratio and abs(rate) >= 0.02 and abs(biananceCoins_rate):
                            try:
                                if percent_rate != listPercentChangeRate[coin['symbol']]:
                                    content = f"Coin:*{coin['symbol']}* {str(rate)}/*{str(round(percent_rate, 2))}%*"
                                    teleContent = teleContent + content + "\n"
                                    listPercentChangeRate[coin['symbol']] = float(percent_rate)
                            except:
                                content = f"Coin:*{coin['symbol']}* {str(rate)}/*{str(round(percent_rate, 2))}%*"
                                teleContent = teleContent + content + "\n"
                                listPercentChangeRate[coin['symbol']] = float(percent_rate)
                    except:
                        pass
    send_message(teleContent)