def close_trade(balance, margin, asset):
    balance = asset*current_price + margin
    asset = 0
    return asset, balance

def start_trade(balance, entry_price):
    asset = balance / entry_price
    balance = 0
    return asset, balance

def value_generator(i):
    
    n1 = df["open"][i]
    n2=round(random.uniform(df["low"][i], df["high"][i]), 2)
    n3=round(random.uniform(df["low"][i], df["high"][i]), 2)
    n4=round(random.uniform(df["low"][i], df["high"][i]), 2)
    n5=round(random.uniform(df["low"][i], df["high"][i]), 2)
    n6=df["close"][i]

    return n1, n2, n3, n4, n5, n6