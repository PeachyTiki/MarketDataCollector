Market Data Collector

Overview

The Market Data Collector is a Python-based automation bot that fetches stock market data, stores it in an SQLite database, exports it to an Excel file with structured formatting, and generates stock trend analysis using moving averages and Bollinger Bands.

Features

✅ Fetches daily stock data from Alpha Vantage API✅ Stores historical stock data in an SQLite database✅ Exports stock data to Excel, with individual sheets for each stock✅ Generates trend analysis (SMA, EMA, Bollinger Bands) and saves as images✅ Automates execution using Windows Task Scheduler✅ Includes a config.json file for easy customization✅ Creates automatic backups of the database

Installation & Setup

1️⃣ Clone the Repository

# Using HTTPS
git clone https://github.com/YOUR_GITHUB_USERNAME/MarketDataCollector.git

# OR using SSH
git clone git@github.com:YOUR_GITHUB_USERNAME/MarketDataCollector.git

2️⃣ Install Dependencies

Navigate to the project directory and create a virtual environment:

cd MarketDataCollector
python -m venv venv  # Create virtual environment
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows

Then install required Python packages:

pip install -r requirements.txt

3️⃣ Set Up Configuration

Update the config.json file with your Alpha Vantage API key and file paths:

{
    "api_key": "YOUR_ALPHA_VANTAGE_API_KEY",
    "database_file": "stocks_info.db",
    "output_excel": "stock_report.xlsx",
    "backup_folder": "backups"
}

4️⃣ Run the Scripts Manually (For Testing)

python fetch_stock_data.py  # Fetch stock market data
python export_to_excel.py  # Export data to Excel
python analyze_stock_trends.py  # Generate stock trend analysis

5️⃣ Automate with Windows Task Scheduler

Create a Task to Run Daily

Open Task Scheduler → "Create Basic Task"

Set Trigger: Daily at Market Open

Set Action: Start a Program

Browse & select python.exe, then add the script path:

C:\Users\YourUsername\PycharmProjects\MarketDataCollector\fetch_stock_data.py

Repeat the process for export_to_excel.py

Ensure "Run whether user is logged in or not" is checked.

File Structure

MarketDataCollector/
│── fetch_stock_data.py         # Fetches stock data
│── export_to_excel.py          # Exports stock data to Excel
│── analyze_stock_trends.py     # Generates stock analysis plots
│── config.json                 # Stores API key & settings
│── stocks_info.db              # SQLite database
│── backups/                    # Stores automatic database backups
│── analysis_plots/             # Stores stock trend images
│── requirements.txt            # Python dependencies
│── README.md                   # This file

Contributing

Contributions are welcome! Feel free to fork this repository, submit a pull request, or suggest features.
