import typer

from backtesting.backtest_multiple_iterations import backtest_multiple_iterations
from backtesting.backtest import backtest_single
from backtesting.data_collector import data_collector
from backtesting.margin_decision import margin_decision

from src.get_configs import configs

from utils.algo_trading import algo_trading

app = typer.Typer()

@app.command()
def data_gatherer():
    data_collector(configs("csv_name"), configs("symbol"), configs("data_collector_interval"), configs("data_collector_start"), 
                    configs("data_collector_end"), configs("endpoint"), configs("columns"))

@app.command()
def margin_decider():
    margin_decision(configs("backtest_balance"), configs("margin_start"), configs("margin_end"), configs("margin_increase"), configs("csv_name"))

@app.command()
def multi_backtest():
    backtest_multiple_iterations(configs("backtest_iteration_count"), configs("backtest_balance"), configs("csv_name"))

@app.command()
def single_backtest():
    backtest_single(configs("backtest_balance"), configs("csv_name"))

@app.command()
def algorithmic_trading():
    algo_trading(configs("API_KEY"), configs("SECRET_KEY"), configs("symbol"), configs("margin_threshold"))

if __name__ == "__main__":
    app()