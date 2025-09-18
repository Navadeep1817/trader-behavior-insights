# src/prepare_data.py
import os
import pandas as pd

ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(ROOT, 'data')
OUT_DIR = os.path.join(ROOT, 'outputs')
os.makedirs(OUT_DIR, exist_ok=True)

# Correct filenames
trades_fp = os.path.join(DATA_DIR, 'hyperliquid_trades.csv')
fg_fp = os.path.join(DATA_DIR, 'fear_greed.csv')

print("Loading data...")
trades = pd.read_csv(trades_fp, low_memory=False)
fg = pd.read_csv(fg_fp, low_memory=False)

print("Trades columns:", trades.columns.tolist())
print("Fear/Greed columns:", fg.columns.tolist())

# Standardize column names
trades.columns = [c.lower().strip() for c in trades.columns]
fg.columns = [c.lower().strip() for c in fg.columns]

# Ensure classification column exists
if 'classification' not in fg.columns:
    fg.rename(columns={fg.columns[-1]: 'classification'}, inplace=True)

# --- Handle timestamps ---
trade_time_col = None
for c in ['timestamp', 'timestamp ist', 'time', 'date', 'datetime']:
    if c in trades.columns:
        trade_time_col = c
        break

fg_time_col = None
for c in ['timestamp', 'time', 'date', 'datetime']:
    if c in fg.columns:
        fg_time_col = c
        break

if trade_time_col and fg_time_col:
    # Convert both to datetime
    trades[trade_time_col] = pd.to_datetime(trades[trade_time_col], errors="coerce")
    fg[fg_time_col] = pd.to_datetime(fg[fg_time_col], errors="coerce")

    # Drop rows with invalid timestamps
    trades = trades.dropna(subset=[trade_time_col])
    fg = fg.dropna(subset=[fg_time_col])

    # Merge
    merged = pd.merge_asof(
        trades.sort_values(trade_time_col),
        fg.sort_values(fg_time_col),
        left_on=trade_time_col,
        right_on=fg_time_col,
        direction="backward"
    )
else:
    print("⚠️ No common time column, adding classification without merge")
    trades['classification'] = fg['classification'].iloc[0]
    merged = trades

# Save output
out_fp = os.path.join(DATA_DIR, "merged_trades_sentiment.csv")
merged.to_csv(out_fp, index=False)
print("✅ Saved merged dataset to:", out_fp)

# Show preview
print("\n🔍 Preview of merged dataset:")
print(merged.head())
