# src/stats_and_model.py
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

ROOT = os.path.join(os.path.dirname(__file__), '..')
DATA_DIR = os.path.join(ROOT, 'data')
OUT_DIR = os.path.join(ROOT, 'outputs')
os.makedirs(OUT_DIR, exist_ok=True)

data_fp = os.path.join(DATA_DIR, "merged_trades_sentiment.csv")

print("Loading merged dataset...")
df = pd.read_csv(data_fp)

print("Columns in dataset:", df.columns.tolist())
print("Sample rows:\n", df.head())

# --- Sentiment handling ---
if "classification" not in df.columns:
    raise KeyError("❌ No 'classification' column found. Please check prepare_data.py output.")

df["classification"] = df["classification"].fillna("unknown")
le_sent = LabelEncoder()
df["sentiment_code"] = le_sent.fit_transform(df["classification"])
print("Sentiment unique classes:", le_sent.classes_)

# --- Features ---
# Side
side_col = None
for c in ["side", "direction"]:
    if c in df.columns:
        side_col = c
        break
if side_col is None:
    df["side"] = "unknown"
    side_col = "side"
le_side = LabelEncoder()
df["side_code"] = le_side.fit_transform(df[side_col].astype(str))

# Leverage (if missing, default 1)
if "leverage" not in df.columns:
    df["leverage"] = 1.0
df["leverage"] = pd.to_numeric(df["leverage"], errors="coerce").fillna(1.0)

# Size (try "size usd", fallback "size tokens")
size_col = None
for c in ["size usd", "size tokens", "size"]:
    if c in df.columns:
        size_col = c
        break
if size_col is None:
    df["size"] = 0.0
    size_col = "size"
df["size"] = pd.to_numeric(df[size_col], errors="coerce").fillna(0.0)

# Closed PnL
pnl_col = None
for c in ["closed pnl", "pnl", "profit"]:
    if c in df.columns:
        pnl_col = c
        break
if pnl_col is None:
    df["closed pnl"] = 0.0
    pnl_col = "closed pnl"
df[pnl_col] = pd.to_numeric(df[pnl_col], errors="coerce").fillna(0.0)

# Target: profitable trade
df["profitable"] = (df[pnl_col] > 0).astype(int)

# --- Build feature matrix ---
features = ["sentiment_code", "side_code", "leverage", "size"]
X = df[features]
y = df["profitable"]

# Scale numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- Train/test split ---
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# --- Model ---
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# --- Evaluation ---
y_pred = model.predict(X_test)

print("\n✅ Model Training Complete")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# --- Save outputs ---
coef_out = os.path.join(OUT_DIR, "logistic_coefficients.csv")
coef_df = pd.DataFrame({
    "feature": features,
    "coefficient": model.coef_[0]
})
coef_df.to_csv(coef_out, index=False)
print("📂 Coefficients saved to:", coef_out)
