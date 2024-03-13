import random

def open_position():
    side = random.choice(['sell', 'buy'])
    return side

def close_position(margin_threshold, symbol_data, symbol):
    margin =round(float(next(item for item in symbol_data if item['symbol'] == symbol)["unrealizedProfit"]),4)
    if margin_threshold <= margin:
        margin_realization = True
    else:
        margin_realization = False
    return margin, margin_realization