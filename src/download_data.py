# Download data script
# src/download_data.py
import os
import gdown

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Drive file IDs from the assignment
# Historical trader data (Hyperliquid) - replace with the file id you were given
HIST_ID = "1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs"
FEARGREED_ID = "1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf"

hist_out = os.path.join(DATA_DIR, 'hyperliquid_trades.csv')
fg_out = os.path.join(DATA_DIR, 'fear_greed.csv')

print("Downloading historical trader data...")
gdown.download(id=HIST_ID, output=hist_out, quiet=False)
print("Downloading fear/greed index...")
gdown.download(id=FEARGREED_ID, output=fg_out, quiet=False)

print("Downloaded to", DATA_DIR)
