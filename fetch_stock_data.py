import json
import sqlite3
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

# ✅ Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

api_key = config["api_key"]
stock_symbols = config["stocks"]
database = config["database"]

# ✅ Connect to SQLite database
conn = sqlite3.connect(database)
cursor = conn.cursor()

# ✅ Create table if it doesn’t exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_data (
        Stock_Symbol TEXT,
        Date TEXT,
        Open REAL,
        High REAL,
        Low REAL,
        Close REAL,
        Volume INTEGER,
        PRIMARY KEY (Stock_Symbol, Date))
''')

# Initialize Alpha Vantage API
ts = TimeSeries(key=api_key, output_format="pandas")

# ✅ Fetch last 2 days of data for each stock
for stock_symbol in stock_symbols:
    try:
        data, meta_data = ts.get_daily(symbol=stock_symbol, outputsize="compact")

        if data.empty:
            print(f"⚠ {stock_symbol}: No data returned. Alpha Vantage may have blocked requests.")
            continue

        # Rename columns to match the database schema
        data = data.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })

        # Add the stock symbol and reset the index
        data["Stock_Symbol"] = stock_symbol
        data = data.reset_index()

        # Convert the 'date' column to a string
        data["Date"] = data["date"].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else None)

        # Keep only the last 2 days
        data = data.head(2)

        print(f"📊 Fetched stock data for {stock_symbol}:\n", data)

        # ✅ Insert only new data
        for index, row in data.iterrows():
            cursor.execute("SELECT COUNT(*) FROM stock_data WHERE Stock_Symbol = ? AND Date = ?",
                           (row["Stock_Symbol"], row["Date"]))
            data_exists = cursor.fetchone()[0]

            if not data_exists:
                cursor.execute('''
                    INSERT INTO stock_data (Stock_Symbol, Date, Open, High, Low, Close, Volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (row["Stock_Symbol"], row["Date"], row["Open"], row["High"], row["Low"], row["Close"],
                      row["Volume"]))
                print(f"✅ Added {stock_symbol} data for {row['Date']} to the database.")
            else:
                print(f"⚠ Data for {stock_symbol} on {row['Date']} already exists. Skipping.")

    except Exception as e:
        print(f"❌ Error fetching {stock_symbol}: {e}")

# ✅ Commit changes and close connection
conn.commit()
conn.close()
print("✅ Stock data update completed.")
