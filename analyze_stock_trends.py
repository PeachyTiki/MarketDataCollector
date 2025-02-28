import json
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# ✅ Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

database = config["database_file"]

# ✅ Connect to SQLite database
conn = sqlite3.connect(database)

# ✅ Read stock data from the database
query = "SELECT * FROM stock_data ORDER BY Date"
df = pd.read_sql(query, conn)

# ✅ Convert Date column to datetime format
df["Date"] = pd.to_datetime(df["Date"])

# ✅ Close database connection
conn.close()

# ✅ Ensure the analysis_plots directory exists & clear previous images
analysis_folder = "analysis_plots"
if not os.path.exists(analysis_folder):
    os.makedirs(analysis_folder)
else:
    # Remove old plots before generating new ones
    for file in os.listdir(analysis_folder):
        file_path = os.path.join(analysis_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

# ✅ Get unique stock symbols
stocks = df["Stock_Symbol"].unique()

# ✅ Loop through each stock and analyze separately
for stock in stocks:
    stock_df = df[df["Stock_Symbol"] == stock].copy()  # Filter data for one stock

    # ✅ Ensure there are at least 20 data points
    if len(stock_df) < 20:
        print(f"⚠ Skipping {stock} - Not enough data for analysis.")
        continue

    # ✅ Calculate Moving Averages
    stock_df["SMA_20"] = stock_df["Close"].rolling(window=20).mean()
    stock_df["EMA_20"] = stock_df["Close"].ewm(span=20, adjust=False).mean()

    # ✅ Calculate Bollinger Bands
    stock_df["Rolling_STD"] = stock_df["Close"].rolling(window=20).std()
    stock_df["Upper_Band"] = stock_df["SMA_20"] + (1.96 * stock_df["Rolling_STD"])
    stock_df["Lower_Band"] = stock_df["SMA_20"] - (1.96 * stock_df["Rolling_STD"])

    # ✅ Drop NaN values to avoid blank plots
    stock_df.dropna(inplace=True)

    # ✅ Plot the stock price and indicators
    plt.figure(figsize=(12, 6))
    plt.plot(stock_df["Date"], stock_df["Close"], label="Close Price", color="blue")
    plt.plot(stock_df["Date"], stock_df["SMA_20"], label="20-Day SMA", linestyle="dashed", color="orange")
    plt.plot(stock_df["Date"], stock_df["EMA_20"], label="20-Day EMA", linestyle="dashed", color="green")
    plt.fill_between(stock_df["Date"], stock_df["Upper_Band"], stock_df["Lower_Band"], color="gray", alpha=0.2, label="Bollinger Bands")

    # Add title and labels
    plt.title(f"{stock} - Stock Trend Analysis with SMA, EMA, and Bollinger Bands")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.grid()

    # ✅ Save the plot as an image (overwrite existing)
    plot_path = os.path.join(analysis_folder, f"{stock}_trend_analysis.png")
    plt.savefig(plot_path, format="png", dpi=300, bbox_inches="tight")
    plt.close()  # Ensure the figure is closed to free memory

    print(f"✅ Analysis saved: {plot_path}")

print("✅ Stock trend analysis completed.")
