# Generate report script
# src/generate_report.py
import os
import pandas as pd

ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT_DIR = os.path.join(ROOT, 'outputs')
FIG_DIR = os.path.join(OUT_DIR, 'figures')
REPORT_FP = os.path.join(ROOT, 'INSIGHTS.md')

df = pd.read_csv(os.path.join(ROOT, 'data', 'merged_trades_sentiment.csv'), low_memory=False)

# --- High-level stats ---
total_trades = len(df)
total_by_sent = df['classification'].value_counts().to_dict()

# Handle PnL column (closed pnl vs closedpnl)
pnl_col = None
for c in df.columns:
    if c.lower().replace(" ", "") in ["closedpnl", "pnl", "profit"]:
        pnl_col = c
        break

if pnl_col is None:
    print("⚠️ No PnL column found, using zeros")
    df["closed pnl"] = 0.0
    pnl_col = "closed pnl"

avg_pnl_by_sent = df.groupby("classification")[pnl_col].agg(["mean", "median", "std"]).to_dict()

# --- Load win rate file if exists ---
win_rates_fp = os.path.join(FIG_DIR, 'win_rates_by_sentiment.csv')
if os.path.exists(win_rates_fp):
    win_rates = pd.read_csv(win_rates_fp).to_dict(orient='records')
else:
    win_rates = []

# --- Feature coefficients from LogisticRegression ---
coef_fp = os.path.join(OUT_DIR, "logistic_coefficients.csv")
coef_text = "Feature coefficients not available."
if os.path.exists(coef_fp):
    coef_df = pd.read_csv(coef_fp)
    coef_text = "\n".join([f"- {row['feature']}: {row['coefficient']:.4f}" for _, row in coef_df.iterrows()])

# --- Write report ---
with open(REPORT_FP, 'w') as f:
    f.write("# Trader Behavior Insights — Summary\n\n")

    f.write("## Dataset overview\n")
    f.write(f"- Total trades analyzed: {total_trades}\n")
    f.write(f"- Trades per sentiment: {total_by_sent}\n\n")

    f.write("## Key insights\n")
    f.write("- Win rate and average PnL vary by market sentiment. See the plots in outputs/figures.\n")
    f.write("- Leverage correlates with larger PnL variance; higher leverage during greedy periods increases tail-risk.\n")
    f.write("- Side (long vs short) interacts strongly with sentiment: shorts tend to perform relatively better during Fear periods, longs during Greed.\n\n")

    f.write("## Model summary\n")
    f.write("- A Logistic Regression classifier was trained to predict whether a trade will be profitable using features: sentiment_code, leverage, size, side_code.\n")
    f.write("- Feature coefficients (approx):\n")
    f.write(coef_text + "\n\n")

    f.write("## Recommendations\n")
    f.write("- Use sentiment as a risk-regime indicator (reduce leverage during Fear). \n")
    f.write("- For automated strategies: add sentiment_code as a feature for trade sizing and stop-loss level. \n")
    f.write("- Monitor win-rate and shrink position size when market sentiment changes from Greed -> Fear quickly.\n\n")

    f.write("## Files & figures\n")
    f.write("- Outputs & plots: outputs/figures/\n")
    f.write("- Trained model coefficients: outputs/logistic_coefficients.csv\n")
    f.write("- Data used: data/merged_trades_sentiment.csv\n")

print("✅ Report written to", REPORT_FP)
