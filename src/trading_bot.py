import importlib

class TradingBot:
    def __init__(self, api_key, api_secret, symbols, grid_step, leverage, commission, initial_capital, target_profit, strategy='init_strat'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.symbols = symbols
        self.grid_step = grid_step
        self.leverage = leverage
        self.commission = commission
        self.initial_capital = initial_capital
        self.target_profit = target_profit
        self.state = {symbol: {'position_size': 0, 'entry_price': 0, 'last_price': 0} for symbol in symbols}
        # Stratejiyi yükle
        self.strategy = self.load_strategy(strategy)

    def load_strategy(self, strategy_name):
        """Belirtilen stratejiyi dinamik olarak yükler."""
        try:
            module = importlib.import_module(f'strategies.{strategy_name}')
            return module.decide_trade
        except ImportError:
            raise ValueError(f"Strategy {strategy_name} not found.")

    def manage_trading(self, symbol, current_price):
        """Trade yönetimini stratejiye göre yapar."""
        s = self.state[symbol]
        if s['position_size'] == 0:
            # Stratejiye göre trade yapılıp yapılmayacağına karar ver
            if self.strategy(current_price, s['last_price'], self.grid_step):
                # Trade işlemleri (örneğin pozisyon açma)
                s['position_size'] = (self.initial_capital * self.leverage) / current_price
                s['entry_price'] = current_price
                s['last_price'] = current_price
                print(f"Opening position for {symbol} at {current_price}")
        elif abs((current_price - s['entry_price']) / s['entry_price']) >= self.target_profit:
            # Pozisyonu kapatma mantığı (değişmedi)
            profit = (current_price - s['entry_price']) * s['position_size'] * self.leverage
            s['position_size'] = 0
            s['entry_price'] = 0
            s['last_price'] = current_price
            print(f"Closing position for {symbol} at {current_price}, Profit: {profit}")
        else:
            s['last_price'] = current_price