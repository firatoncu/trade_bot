import random 
from statistics import mean 

margin_list = []
iteration_count = 10

def close_trade(balance, margin, asset):
    balance = asset*current_price + margin
    asset = 0
    return asset, balance

def start_trade(balance, entry_price):
    asset = balance / entry_price
    balance = 0
    return asset, balance

for x in range (0,iteration_count):
    entry_price = 0
    position_type = None
    balance = 100
    starting_balance = balance

    for i in range (0,len(df)):

        n1 = df["open"][i]
        n2=round(random.uniform(df["low"][i], df["high"][i]), 2)
        n3=round(random.uniform(df["low"][i], df["high"][i]), 2)
        n4=round(random.uniform(df["low"][i], df["high"][i]), 2)
        n5=round(random.uniform(df["low"][i], df["high"][i]), 2)
        n6=df["open"][i]

        for node in (n1, n2, n3, n4, n5, n6):
            current_price = node
            if entry_price != 0:
                margin = asset*(current_price - entry_price) if position_type == 'long' else asset*(entry_price - current_price)
                if (margin > 1):
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
    print(f"Your balance moved from ${starting_balance} to ${round(balance,2)} in {x+1}. iteration Your total earning is ${gross_margin}")
    
    margin_list.append(gross_margin)

print(f"In total of {iteration_count} iterations: Your average gross margin is {round(sum(margin_list)/iteration_count,2)}.")
print(f"Maximum gross margin was: {max(margin_list)}")
print(f"Minimum gross margin was: {min(margin_list)}")
print(f"You can find each of your gross margin values in dollars.")
print(margin_list)