import pandas as pd

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