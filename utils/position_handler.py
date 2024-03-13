import ccxt
from binance.client import Client
from datetime import datetime
from utils.strategies import open_position


def handle_position(API_KEY, SECRET_KEY, symbol, symbol_data, random_choice):
    # Initialize Binance USDM futures exchange
    exchange = ccxt.binanceusdm({
        'apiKey': API_KEY,
        'secret': SECRET_KEY,
    })
    client = Client(API_KEY, SECRET_KEY)
    current_price = round(float(client.get_symbol_ticker(symbol=symbol)['price']), 3)
    current_balance = round(float(next(item for item in client.futures_account_balance() if item['asset'] == "USDT")["balance"])-0.001,3)
    
    # Fetch all open positions
    position = next(item for item in symbol_data if item['symbol'] == symbol)
    
    # Close each position at market price
    
    symbol = position['symbol']
    amount = float(position['positionAmt'])
    side = 'sell' if amount > 0 else 'buy'  # Close long positions with 'sell', short positions with 'buy'
    if random_choice == True:
        side = open_position()
        amount = current_balance / current_price

    try:
        closing_order = exchange.create_order(symbol, 'market', side, abs(amount), None)
        if side == "sell":
            print(f"Short position opened from {current_balance} dollars with price of {current_price}")
        else:
            print(f"Long position opened from {current_balance} dollars with price of {current_price}. ")
    except Exception as e:
        print(f"Error closing position for {symbol}: {type(e).__name__} - {str(e)}")