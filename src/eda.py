# src/eda.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(ROOT, 'data')
OUT_DIR = os.path.join(ROOT, 'outputs')
FIG_DIR = os.path.join(OUT_DIR, 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# Load CSV
df = pd.read_csv(os.path.join(DATA_DIR, "merged_trades_sentiment.csv"))

# --- Handle PnL column ---
pnl_col = None
for c in df.columns:
    if c.lower().replace(" ", "") in ["closedpnl", "pnl", "profit"]:
        pnl_col = c
        break
if pnl_col is None:
    df["closed pnl"] = 0.0
    pnl_col = "closed pnl"

# --- Create 'profitable' column ---
df["profitable"] = df[pnl_col] > 0

# --- 1. Trades per sentiment ---
plt.figure(figsize=(6,4))
sns.countplot(x="classification", data=df)
plt.title("Trades per Sentiment")
plt.savefig(os.path.join(FIG_DIR, "trades_per_sentiment.png"))
plt.close()

# --- 2. Avg PnL per sentiment ---
plt.figure(figsize=(6,4))
sns.barplot(x="classification", y=pnl_col, data=df, estimator=lambda x: sum(x)/len(x))
plt.title("Average PnL per Sentiment")
plt.savefig(os.path.join(FIG_DIR, "avg_pnl_per_sentiment.png"))
plt.close()

# --- 3. Win rate by sentiment ---
win_rates = df.groupby("classification")["profitable"].mean() * 100
plt.figure(figsize=(6,4))
win_rates.plot(kind="bar", title="Win Rate by Sentiment")
plt.ylabel("Win Rate (%)")
plt.savefig(os.path.join(FIG_DIR, "win_rate_by_sentiment.png"))
plt.close()

# --- 4. PnL vs leverage ---
if "leverage" in df.columns:
    plt.figure(figsize=(6,4))
    sns.scatterplot(x="leverage", y=pnl_col, hue="classification", data=df, alpha=0.5)
    plt.title("PnL vs Leverage by Sentiment")
    plt.savefig(os.path.join(FIG_DIR, "pnl_vs_leverage.png"))
    plt.close()

# --- 5. Side × Sentiment ---
if "side" in df.columns:
    pivot = df.groupby(["classification","side"])["profitable"].mean().unstack()
    plt.figure(figsize=(6,4))
    pivot.plot(kind="bar", title="Win Rate by Side × Sentiment")
    plt.ylabel("Win Rate")
    plt.savefig(os.path.join(FIG_DIR, "side_sentiment_winrate.png"))
    plt.close()

# --- 6. Feature Coefficients ---
coef_fp = os.path.join(OUT_DIR, "logistic_coefficients.csv")
if os.path.exists(coef_fp):
    coef_df = pd.read_csv(coef_fp)
    plt.figure(figsize=(6,4))
    sns.barplot(x="coefficient", y="feature", data=coef_df, orient="h")
    plt.title("Logistic Regression Feature Coefficients")
    plt.savefig(os.path.join(FIG_DIR, "feature_coefficients.png"))
    plt.close()

print("✅ Figures saved in:", FIG_DIR)
