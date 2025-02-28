import time
import logging
import threading
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
from .utils import adjust_to_tick_size, get_symbol_precision

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class TradingBot:
    def __init__(self, api_key, api_secret, symbols, grid_step, leverage, commission, initial_capital, target_profit):
        self.client = Client(api_key, api_secret)
        self.client.API_URL = 'https://fapi.binance.com'
        self.symbols = symbols
        self.grid_step = grid_step
        self.leverage = leverage
        self.commission = commission
        self.initial_capital = initial_capital
        self.capital_per_asset = initial_capital / len(symbols)
        self.target_profit = target_profit
        self.running = False
        self.lock = threading.Lock()

        # Symbol precisions
        self.symbol_precisions = {symbol: get_symbol_precision(self.client, symbol) for symbol in symbols}

        # State initialization
        self.state = {
            symbol: {
                'capital': self.capital_per_asset,
                'position_size': 0,
                'entry_price': None,
                'grid_levels': {},
                'last_price': None,
                'transactions': 0,
                'open_orders': {}
            } for symbol in symbols
        }

    def start(self):
        self.running = True
        for symbol in self.symbols:
            try:
                self.client.futures_change_leverage(symbol=symbol, leverage=self.leverage)
                logging.info(f"{symbol} için kaldıraç {self.leverage}x olarak ayarlandı")
            except Exception as e:
                logging.error(f"{symbol} için kaldıraç ayarı hatası: {e}")

        while self.running:
            for symbol in self.symbols:
                try:
                    ticker = self.client.futures_symbol_ticker(symbol=symbol)
                    current_price = float(ticker['price'])
                    s = self.state[symbol]
                    if s['last_price'] is None:
                        s['last_price'] = current_price

                    self.check_orders(symbol)
                    self.manage_trading(symbol, current_price)
                except Exception as e:
                    logging.error(f"{symbol} işlenirken hata: {e}")
            time.sleep(2)

    def stop(self):
        self.running = False

    def place_order(self, symbol, side, price, quantity):
        price_prec, qty_prec, _ = self.symbol_precisions[symbol]
        price_str = f"{price:.{price_prec}f}"
        quantity_str = f"{quantity:.{qty_prec}f}"
        try:
            order = self.client.futures_create_order(
                symbol=symbol, side=side, type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC, quantity=quantity_str, price=price_str
            )
            logging.info(f"{symbol} için {side} emri: {price_str}, Miktar: {quantity_str}")
            return order['orderId']
        except Exception as e:
            logging.error(f"{symbol} için emir hatası: {e}")
            return None

    def cancel_order(self, symbol, order_id):
        try:
            self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            logging.info(f"{symbol} için emir {order_id} iptal edildi")
        except Exception as e:
            logging.error(f"{symbol} için emir iptal hatası: {e}")

    def check_orders(self, symbol):
        s = self.state[symbol]
        for order_id in list(s['open_orders'].keys()):
            try:
                order = self.client.futures_get_order(symbol=symbol, orderId=order_id)
                if order['status'] == 'FILLED':
                    price = float(order['price'])
                    qty = float(order['origQty'])
                    side = order['side']
                    if side == SIDE_BUY and s['position_size'] == 0:
                        s['position_size'] = qty
                        s['entry_price'] = price
                        s['capital'] -= (self.capital_per_asset * self.leverage * self.commission)
                    elif side == SIDE_SELL and s['position_size'] > 0:
                        profit = (price - s['entry_price']) * s['position_size']
                        s['capital'] += profit - (self.capital_per_asset * self.leverage * self.commission)
                        s['position_size'] = 0
                        s['transactions'] += 1
                    elif side == SIDE_SELL and s['position_size'] == 0:
                        s['position_size'] = -qty
                        s['entry_price'] = price
                        s['capital'] -= (self.capital_per_asset * self.leverage * self.commission)
                    elif side == SIDE_BUY and s['position_size'] < 0:
                        profit = (s['entry_price'] - price) * abs(s['position_size'])
                        s['capital'] += profit - (self.capital_per_asset * self.leverage * self.commission)
                        s['position_size'] = 0
                        s['transactions'] += 1
                    del s['open_orders'][order_id]
            except Exception as e:
                logging.error(f"{symbol} için emir kontrol hatası: {e}")

    def manage_trading(self, symbol, current_price):
        s = self.state[symbol]
        tick_size = self.symbol_precisions[symbol]['tick_size']
        position_value = self.capital_per_asset * self.leverage

        if s['position_size'] == 0:
            if abs((current_price - s['last_price']) / s['last_price']) > self.grid_step:
                for order_id in list(s['open_orders'].keys()):
                    self.cancel_order(symbol, order_id)
                    del s['open_orders'][order_id]
                s['grid_levels'].clear()
                base_price = current_price
                for level in range(-5, 6):
                    if level == 0:
                        continue
                    price = base_price * (1 + level * self.grid_step)
                    adjusted_price = adjust_to_tick_size(price, tick_size, 'down' if level < 0 else 'up')
                    qty = position_value / adjusted_price
                    side = SIDE_BUY if level < 0 else SIDE_SELL
                    order_id = self.place_order(symbol, side, adjusted_price, qty)
                    if order_id:
                        s['open_orders'][order_id] = {'price': adjusted_price, 'side': side}
                s['last_price'] = current_price
        elif s['position_size'] > 0:
            target_sell_price = s['entry_price'] * (1 + self.target_profit + 2 * self.commission)
            adjusted_sell_price = adjust_to_tick_size(target_sell_price, tick_size, 'up')
            if not s['open_orders']:
                order_id = self.place_order(symbol, SIDE_SELL, adjusted_sell_price, s['position_size'])
                if order_id:
                    s['open_orders'][order_id] = {'price': adjusted_sell_price, 'side': SIDE_SELL}
        elif s['position_size'] < 0:
            target_buy_price = s['entry_price'] * (1 - self.target_profit - 2 * self.commission)
            adjusted_buy_price = adjust_to_tick_size(target_buy_price, tick_size, 'down')
            if not s['open_orders']:
                order_id = self.place_order(symbol, SIDE_BUY, adjusted_buy_price, abs(s['position_size']))
                if order_id:
                    s['open_orders'][order_id] = {'price': adjusted_buy_price, 'side': SIDE_BUY}

    def get_status(self):
        with self.lock:
            status = {
                'running': self.running,
                'total_equity': 0,
                'symbols': {}
            }
            for symbol, s in self.state.items():
                try:
                    current_price = float(self.client.futures_symbol_ticker(symbol=symbol)['price'])
                    unrealized_pnl = 0
                    if s['position_size'] > 0:
                        unrealized_pnl = (current_price - s['entry_price']) * s['position_size']
                    elif s['position_size'] < 0:
                        unrealized_pnl = (s['entry_price'] - current_price) * abs(s['position_size'])
                    equity = s['capital'] + unrealized_pnl
                    status['symbols'][symbol] = {
                        'equity': equity,
                        'position_size': s['position_size'],
                        'entry_price': s['entry_price'],
                        'transactions': s['transactions']
                    }
                    status['total_equity'] += equity
                except Exception as e:
                    status['symbols'][symbol] = {'error': str(e)}
            return status