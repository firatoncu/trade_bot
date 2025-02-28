import os
import sys
import threading
from flask import Flask, render_template, request, jsonify

# Proje kök dizinini sys.path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.trading_bot import TradingBot
from src.config import default_config

app = Flask(__name__, template_folder='templates', static_folder='static')

bot = None
bot_thread = None
config = default_config.copy()


@app.route('/')
def index():
    status = bot.get_status() if bot else {'running': False}
    return render_template('index.html', status=status, config=config)

@app.route('/start', methods=['POST'])
def start_bot():
    global bot, bot_thread
    if bot is None:
        bot = TradingBot(**config)
        bot_thread = threading.Thread(target=bot.start)
        bot_thread.start()
        return jsonify({'message': 'Bot başlatıldı'})
    return jsonify({'message': 'Bot zaten çalışıyor'})

@app.route('/stop', methods=['POST'])
def stop_bot():
    global bot, bot_thread
    if bot is not None:
        bot.stop()
        bot_thread.join()
        bot, bot_thread = None, None
        return jsonify({'message': 'Bot durduruldu'})
    return jsonify({'message': 'Bot çalışmıyor'})

@app.route('/update_config', methods=['POST'])
def update_config():
    global config
    if bot is None:
        config['symbols'] = request.form.get('symbols').split(',')
        config['grid_step'] = float(request.form.get('grid_step'))
        config['leverage'] = int(request.form.get('leverage'))
        config['commission'] = float(request.form.get('commission'))
        config['initial_capital'] = float(request.form.get('initial_capital'))
        config['target_profit'] = float(request.form.get('target_profit'))
        return jsonify({'message': 'Yapılandırma güncellendi'})
    return jsonify({'message': 'Bot çalışırken yapılandırma güncellenemez'})

@app.route('/status')
def get_status():
    return jsonify(bot.get_status() if bot else {'running': False})

if __name__ == '__main__':
    app.run(debug=True)