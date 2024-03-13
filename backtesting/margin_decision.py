import random 
import pandas as pd
from statistics import mean 
import numpy as np
from utils.backtest_trading import close_trade, start_trade, value_generator
from src.get_configs import configs

def margin_decision(balance, start_point, end_point, increasement, csv_name):
    margin_list = []
    df = pd.read_csv(csv_name)
    for margin_threshold in(np.arange(start_point, end_point, increasement)):
        margin_threshold = round(margin_threshold,2)
        for x in range (0,iteration_count):
            entry_price = 0
            position_type = None
            starting_balance = balance

            for i in range (0,len(df)):

                n1, n2, n3, n4, n5, n6 = value_generator(i)

                for node in (n1, n2, n3, n4, n5, n6):
                    current_price = node
                    if entry_price != 0:
                        margin = asset*(current_price - entry_price) if position_type == 'long' else asset*(entry_price - current_price)
                        if (margin > margin_threshold):
                            asset, balance = close_trade(balance, margin, asset)
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

                        # Randomly decide whether to go long or short
            if (entry_price != 0):
                balance = round(asset*entry_price,2)
            else:
                balance = round(balance,2)
            gross_margin = round(balance-100,2)

            margin_list.append(gross_margin)
        print("")
        print(f"##### Margin > {margin_threshold} #####")
        print(f"In total of {iteration_count} iterations: Your average gross margin is {round(sum(margin_list)/iteration_count,2)}.")
        print(f"Maximum gross margin was: {max(margin_list)}")
        print(f"Minimum gross margin was: {min(margin_list)}")
        print("")