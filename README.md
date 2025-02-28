
# Crypto Trading Bot

This repository contains a **Crypto Trading Bot** designed for automated futures trading on Binance. The bot leverages the Binance API to execute trades based on configurable parameters and provides a web-based interface for managing trading operations. Built with Python and Flask, it aims to simplify cryptocurrency trading by offering real-time monitoring and easy configuration through an UI.

## Purpose
The primary purpose of this bot is to automate cryptocurrency futures trading on Binance. It allows users to:
- Define trading parameters such as symbols, leverage, and profit targets.
- Start and stop trading operations via a user-friendly web dashboard.
- Monitor trading status, including equity and positions, in real time.

This tool is ideal for traders looking to automate their strategies while maintaining control over key settings.

## Installation

### Prerequisites
- Python 3.8 or higher
- Binance API Key and Secret (obtainable from your Binance account)
- A Binance account with futures trading enabled

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/firatoncu/trade_bot.git
   cd trade_bot
   ```

2. **Install Dependencies**: Ensure you have pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```


3. **Configure API Keys**: 
-   Open the src/config.py file in a text editor.  
-   Replace the placeholder API key and secret with your own Binance credentials:
   ```python
default_config = {
    'api_key': 'your_api_key_here',
    'api_secret': 'your_api_secret_here',
    'symbols': ['BNBUSDT', 'ETHUSDT'],
    'grid_step': 0.0012,
    'leverage': 3,
    'commission': 0.0002,
    'initial_capital': 100,
    'target_profit': 0.0015
}
   ```

4. **Run**:
* Navigate to the web directory: 
   ```bash
   cd web
   python app.py