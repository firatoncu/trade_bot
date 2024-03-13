import requests
import pandas as pd

# Define the Binance API endpoint for klines (historical data)
endpoint = "https://api.binance.com/api/v3/klines"

# Set the parameters for the request
symbol = "BNBUSDT"  # BNB/USDT trading pair
interval = "1s"     # 1-second interval
start_time = 1646082000000  # Unix timestamp for March 1, 2023, 00:00:00 UTC
end_time = 1677704399999    # Unix timestamp for March 1, 2023, 23:59:59 UTC
columns = ["timestamp", "open", "high", "low", "close", "volume", "close_time", 
          "quote_asset_volume", "num_trades", "taker_buy_base_asset_volume", 
          "taker_buy_quote_asset_volume",  "ignore"]

def df_operations(df):
    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["timestamp_rounded"] = pd.to_datetime(df["timestamp"], unit="ms").astype('datetime64[s]').round('10s')
    df[["open","high","low", "close"]] = df[["open","high","low", "close"]].astype(float)
    
    df_open = df.loc[df.groupby('timestamp_rounded')['timestamp'].transform(min) == df["timestamp"]]
    df_close = df.loc[df.groupby('timestamp_rounded')['timestamp'].transform(max) == df["timestamp"]]
    df_high = df.loc[df.groupby('timestamp_rounded')['high'].transform(max) == df["high"]]
    df_high = df_high.drop_duplicates(subset=['timestamp_rounded'], keep='last')
    df_low = df.loc[df.groupby('timestamp_rounded')['low'].transform(min) == df["low"]]
    df_low = df_low.drop_duplicates(subset=['timestamp_rounded'], keep='last')
    
    df_open_close = pd.merge(df_open[["open", "timestamp_rounded"]], df_close[["close", "timestamp_rounded"]], 
                                on=["timestamp_rounded"], how="inner")
    df_high_low = pd.merge(df_high[["high", "timestamp_rounded"]], df_low[["low", "timestamp_rounded"]], 
                                on=["timestamp_rounded"], how="inner")
    df = pd.merge(df_open_close[["open","close","timestamp_rounded"]], df_high_low[["high","low","timestamp_rounded"]],
                    on=["timestamp_rounded"], how="inner")
        
    return df

def data_collector(symbol, interval, start_time, end_time, endpoint, columns):
    for i in range(0,end_time-start_time,300000):
        params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time+i,
        "endTime": end_time,
        "limit": 300
        }
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()

            df = pd.DataFrame(data, columns=columns)
            df = df_operations(df)

            # Save the relevant columns to a CSV file
            if i == 0:
                df.to_csv("bnb_usdt_march1_2023.csv", index=False)
            else:
                df.to_csv("bnb_usdt_march1_2023.csv", mode="a", index=False, header=False)


            print(f"Data saved to bnb_usdt_march1_2023.csv")

        except requests.RequestException as e:
            print(f"Error fetching data: {e}")

data_collector(symbol, interval, start_time, end_time, endpoint, columns)
