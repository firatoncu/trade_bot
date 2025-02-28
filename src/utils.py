from decimal import Decimal, ROUND_DOWN, ROUND_UP

def adjust_to_tick_size(price, tick_size, direction='nearest'):
    price = Decimal(str(price))
    tick_size = Decimal(str(tick_size))
    if direction == 'nearest':
        adjusted = (price / tick_size).quantize(Decimal('1.'), rounding=ROUND_DOWN) * tick_size
    elif direction == 'up':
        adjusted = (price / tick_size).quantize(Decimal('1.'), rounding=ROUND_UP) * tick_size
    elif direction == 'down':
        adjusted = (price / tick_size).quantize(Decimal('1.'), rounding=ROUND_DOWN) * tick_size
    return float(adjusted)

def get_symbol_precision(client, symbol):
    exchange_info = client.futures_exchange_info()
    for s in exchange_info['symbols']:
        if s['symbol'] == symbol:
            price_prec = s['pricePrecision']
            qty_prec = s['quantityPrecision']
            for f in s['filters']:
                if f['filterType'] == 'PRICE_FILTER':
                    tick_size = float(f['tickSize'])
            return price_prec, qty_prec, tick_size
    raise ValueError(f"Symbol {symbol} exchange bilgilerinde bulunamadı")