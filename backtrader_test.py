import backtrader as bt
import backtrader.feeds as btfeeds
import random

class RandomStrategy(bt.Strategy):
    def __init__(self):
        self.order = None  # To keep track of pending orders

    def next(self):
        if self.order:  # If an order is pending, don't do anything
            return

        # Check if we are in the market
        if self.position:
            # We are already in the market, check if it's time to sell
            if 0.15 <= self.position.pnl <= 1.00:
                self.order = self.sell()

        else:
            # We are not in the market, check if it's time to buy
            if random.choice(['long', 'short']) == 'long':
                self.order = self.buy()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Order submitted/accepted - nothing to do
            return

        # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                print('BUY EXECUTED,', order.executed.price)
            elif order.issell():
                print('SELL EXECUTED,', order.executed.price)

        # Write down that there's no order
        self.order = None

# Create a cerebro entity
cerebro = bt.Cerebro()

# Add a strategy
cerebro.addstrategy(RandomStrategy)

# Load data
data = btfeeds.YahooFinanceData(dataname='BNB-USD', fromdate="2022-01-01", todate="2022-01-05")
cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(100000.0)

# Run over everything
cerebro.run()
