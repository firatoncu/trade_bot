import random 
import pandas as pd
from utils.backtest_trading import close_trade, start_trade, value_generator
from src.get_configs import configs

def backtest_single(balance, csv_name):
    df = pd.read_csv(csv_name)
    entry_price = 0
    position_type = None
    starting_balance = balance

    for i in range (0,len(df)):

        n1, n2, n3, n4, n5, n6 = value_generator(i)

        for node in (n1, n2, n3, n4, n5, n6):
            current_price = node
            if entry_price != 0:
                margin = asset*(current_price - entry_price) if position_type == 'long' else asset*(entry_price - current_price)
                if (margin > 0.15):
                    print(f'Margin: {margin}')
                    asset, balance = close_trade(balance, margin, asset)
                    print(f'Closed {position_type} position with margin of {margin} and value of {current_price}')
                    entry_price = 0
                    position_type = None
                    margin = None
                else:
                    # If the position is not closed, continue to the next iteration
                    continue
            
            else:
                # Place a market buy order (going long)
                entry_price = current_price
                asset, balance = start_trade(balance, entry_price)
                position_type = random.choice(['long', 'short'])
                print("")
                print(f'Started {position_type} position with entry price of {entry_price}')

                # Randomly decide whether to go long or short
    if (entry_price != 0):
        balance = round(asset*entry_price,2)
        print(f'Closed last position without margin.')
    else:
        balance = round(balance,2)
    gross_margin = round(balance-100,2)
    print(f"Your balance moved from ${starting_balance} to ${round(balance,2)} Your total earning is ${gross_margin}")