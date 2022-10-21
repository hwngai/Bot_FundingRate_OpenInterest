import logging
from FundingRate import  *
from price_futures_spot import price
from OpenInterest import openInterest
from FundingRateHistory import fundingRateHistory
from credentials import TELEGRAM_BOT_TOKEN
from telegram_message_sender import send_message
from telegram import ReplyKeyboardRemove, Update
import telegram
from telegram.ext import (
	Updater,
	CommandHandler,
	ConversationHandler,
	CallbackContext,)


logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def help(update: Update, context: CallbackContext) -> int:
	update.message.reply_text(
		'/check \n/Subscribe Symbol calculation valueToCheck \n/UnSubcribe Symbol \n/ListSubscribe',
		reply_markup=ReplyKeyboardRemove(),
	)
	return ConversationHandler.END

def printListSubscribe(content = ""):
	for symbol in sorted(listSubscribe, key=lambda val:val["symbol"]):
		content = content + str(symbol["symbol"]) + " " + str(symbol["calculation"]) + " " + str(symbol["value"]) + ", "
	if len(content) > 0:
		print(content)
		send_message(content)
	else:
		print("Empty")
		send_message("Empty")
		

		
def cmdSubscribe(update, context):
	try:
		value = float(context.args[2])
		calculation = context.args[1]
		if "," in context.args[0]:
			listSymbol = str(context.args[0]).split(",")
			for symbol in listSymbol:
				c = 0
				for idx, subscribe in enumerate(listSubscribe):
					if subscribe["symbol"].lower() == symbol.lower() and subscribe["calculation"] == calculation:
						listSubscribe[idx]["value"] = value
						c = 1
				if c == 0:
					listSubscribe.append({"symbol": symbol, "calculation": calculation, "value": value})
		else:
			symbol = str(context.args[0])
			c = 0
			for idx, subscribe in enumerate(listSubscribe):
				if subscribe["symbol"].lower() == symbol.lower() and subscribe["calculation"] == calculation:
					listSubscribe[idx]["value"] = value
					c = 1
			if c == 0:
				listSubscribe.append({"symbol": symbol, "calculation": calculation, "value": value})
	except (IndexError, ValueError):
		update.message.reply_text('Invalid params: Symbol FundingRate')
	pushMarketFundingRate(TIME = 3, listSubscribe=listSubscribe)
	printListSubscribe(content = "*Lệnh chờ:* ")
		
def cmdUnSubscribe(update, context):
	try:
		if "," in context.args[0]:
			listSymbol = str(context.args[0]).split(",")
			for symbol in listSymbol:
				try: 
					removeSymbol(symbol, calculation = "<")
				except:
					removeSymbol(symbol, calculation = ">")
		else:
			symbol = str(context.args[0])
			removeSymbol(symbol)
	except (IndexError, ValueError):
		update.message.reply_text('Invalid params: Symbol FundingRate')
	printListSubscribe(content = "*Lệnh chờ:* ")
		
def cmdListSubscribe(update, context):
	print(context)
	printListSubscribe()
	
def cancel(update: Update, context: CallbackContext) -> int:
	user = update.message.from_user
	logger.info("User %s canceled the conversation.", user.first_name)
	update.message.reply_text(
		'Bye!', reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END


def cmdCheck(update, context):
	try:
		print(context.args[0])
		if context.args[0].lower() == "all":
			pushMarketFundingRate(TIME = 0, listSubscribe = [{"symbol": "allcoin","calculation":"<", "value": "-0.01"}], c = 1)

		else:
			rate, fundingRate_history = fundingRateHistory(context.args[0])
			openInterest_now, openInterest_history = openInterest(context.args[0])
			price_spot, price_futures,ratio = price(context.args[0])
			Price = f"Price spot:*{price_spot}* futures:*{price_futures}*  ratio:*{ratio}%*"
			fundingRate_text = f"FR: *{rate}* 5m:*{fundingRate_history['m5']}%* 15m:*{fundingRate_history['m15']}%* H1:*{fundingRate_history['H1']}%* H4:*{fundingRate_history['H4']}%*"
			openInterest_text = f"OI: *{round(openInterest_now/1000000,2)}M* 5m:*{openInterest_history['m5']}%* 15m:*{openInterest_history['m15']}%* H1:*{openInterest_history['H1']}%* H4:*{openInterest_history['H4']}%*"
			teleContent = f"Coin: *{context.args[0]}*" + "\n" + fundingRate_text + "\n" + openInterest_text + "\n" + Price
			update.message.reply_text(teleContent, parse_mode=telegram.ParseMode.MARKDOWN)
	except (IndexError, ValueError):
		update.message.reply_text('Invalid params:/check all or Symbol')

	
def get_value_rate():
	global biananceCoins, listPercentChangeRate
	listPercentChangeRate = {}
	threading.Timer(5*60, get_value_rate).start()
	url = 'https://fapi.coinglass.com/api/fundingRate/v2/home'
	resp = req.get(url)
	data = resp.json()
	for coin in data['data']:
		markets = coin["uMarginList"]
		for market in markets:
			if market["exchangeName"] == "Binance":
				if "rate" in market:
					rate = market["rate"]
					openinterest = 0
					biananceCoins[coin["symbol"]] = (float(rate), openinterest)


def main() -> None:
	updater = Updater(TELEGRAM_BOT_TOKEN)
	dispatcher = updater.dispatcher
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('help', help), CommandHandler('subscribe', cmdSubscribe), CommandHandler('unSubscribe', cmdUnSubscribe), CommandHandler('ListSubscribe', cmdListSubscribe), CommandHandler('check', cmdCheck)],
		states={},
		fallbacks=[CommandHandler('cancel', cancel)],)
	dispatcher.add_handler(conv_handler)
	updater.start_polling()
	get_value_rate()
	mutationsFundingRate()
	pushMarketFundingRate(TIME = 30*60 -2, listSubscribe = [{"symbol": "allcoin","calculation":">", "value": "0.01"}])
	pushMarketFundingRate(TIME = 30*60, listSubscribe = [{"symbol": "allcoin","calculation":"<", "value": "-0.01"}])
	printListSubscribe(content = "*Lệnh chờ:* ")
	updater.idle()

						
if __name__ == '__main__':
	main()
	
