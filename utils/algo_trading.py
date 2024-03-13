import random
import time
from binance.client import Client
from binance.cm_futures import CMFutures
from utils.position_handler import handle_position
from utils.strategies import close_position
from src.get_configs import configs

def algo_trading(API_KEY, SECRET_KEY, symbol, margin_threshold):
    cm_futures_client = CMFutures(key=API_KEY, secret=SECRET_KEY)
    client = Client(API_KEY, SECRET_KEY)


    is_order = True

    while True:
        symbol_data = client.futures_account()['positions']
        # Calculate margin if there's an open position
        if is_order is True:
            margin, margin_realization = close_position(margin_threshold, symbol_data, symbol)
            if margin_realization is True:
                handle_position(API_KEY, SECRET_KEY, symbol, symbol_data, False)
                is_order = False
                current_price = round(float(client.get_symbol_ticker(symbol=symbol)['price']), 3)
                current_balance = round(float(next(item for item in client.futures_account_balance() if item['asset'] == "USDT")["balance"])-0.001,3)
                print(f"Reached margin threshold! Closed position with {round(margin,3)} $ margin from {round(current_price,3)} dollars. Final balance is {round(current_balance,3)}")
                print("")
                continue
            else:
                # If the position is not closed, continue to the next iteration
                continue

        # Randomly decide whether to go long or short
        handle_position(API_KEY, SECRET_KEY, symbol, symbol_data, True)
        is_order = True

        # Wait for a while before the next operation to avoid hitting rate limits
        time.sleep(1)  # 100 milliseconds