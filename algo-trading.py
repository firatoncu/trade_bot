import random
import time
from binance.client import Client

client = Client('YOUR_API_KEY', 'YOUR_SECRET_KEY')
symbol = 'BNBUSDT'

# Initialize variables for entry price and position type
entry_price = None
position_type = None

while True:
    # Fetch USDT balance
    usdt_balance = client.get_asset_balance(asset='USDT')
    quantity = float(usdt_balance['free'])  # free amount of USDT

    # Fetch current price
    current_price = float(client.get_symbol_ticker(symbol=symbol)['price'])

    # Calculate margin if there's an open position
    if entry_price is not None:
        margin = current_price - entry_price if position_type == 'long' else entry_price - current_price
        print(f'Margin: {margin}')

        # Close position if margin is between 15 cents and 1 dollar
        if 0.15 <= margin <= 1.00:
            if position_type == 'long':
                order = client.order_market_sell(
                    symbol=symbol,
                    quantity=quantity
                )
            else:
                order = client.order_market_buy(
                    symbol=symbol,
                    quantity=quantity
                )

            print(f'Closed {position_type} position with margin of {margin}')
            entry_price = None
            position_type = None
        else:
            # If the position is not closed, continue to the next iteration
            continue

    # Randomly decide whether to go long or short
    if random.choice(['long', 'short']) == 'long':
        # Place a market buy order (going long)
        order = client.order_market_buy(
            symbol=symbol,
            quantity=quantity
        )
        entry_price = current_price
        position_type = 'long'
    else:
        # Place a market sell order (going short)
        order = client.order_market_sell(
            symbol=symbol,
            quantity=quantity
        )
        entry_price = current_price
        position_type = 'short'

    print(f'Opened {position_type} position at {entry_price}')

    # Wait for a while before the next operation to avoid hitting rate limits
    time.sleep(0.1)  # 100 milliseconds
