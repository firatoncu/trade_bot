import requests
import pandas as pd
from utils.data_collector_opt import df_operations

def data_collector(csv_name, symbol, interval, start_time, end_time, endpoint, columns):
    for i in range(0,end_time-start_time,300):
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
                df.to_csv("data/"+csv_name, index=False)
            else:
                df.to_csv("data/"+csv_name, mode="a", index=False, header=False)


            print(f"Data saved to data/{csv_name}")

        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
