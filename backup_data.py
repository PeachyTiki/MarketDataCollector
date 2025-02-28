import os
import shutil
import datetime
import json

# Load config file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Define paths from config
database_file = config["database_file"]
excel_file = config["excel_file"]
backup_folder = config["backup_folder"]

# Ensure the backup folder exists
os.makedirs(backup_folder, exist_ok=True)

# Create a timestamped backup
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
db_backup_path = os.path.join(backup_folder, f"backup_{timestamp}.db")
excel_backup_path = os.path.join(backup_folder, f"backup_{timestamp}.xlsx")

# Copy the database file
if os.path.exists(database_file):
    shutil.copy(database_file, db_backup_path)
    print(f"✅ Database backed up as: {db_backup_path}")
else:
    print("⚠ No database file found to back up.")

# Copy the Excel file
if os.path.exists(excel_file):
    shutil.copy(excel_file, excel_backup_path)
    print(f"✅ Excel report backed up as: {excel_backup_path}")
else:
    print("⚠ No Excel file found to back up.")

# 🔥 Delete backups older than 7 days
cutoff_time = datetime.datetime.now() - datetime.timedelta(days=7)

for file in os.listdir(backup_folder):
    file_path = os.path.join(backup_folder, file)
    if os.path.isfile(file_path):
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        if file_time < cutoff_time:
            os.remove(file_path)
            print(f"🗑 Deleted old backup: {file_path}")

print("✅ Backup process completed.")
