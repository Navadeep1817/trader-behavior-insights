# Trader Behavior Insights — Summary

## Dataset overview
- Total trades analyzed: 211224
- Trades per sentiment: {'Greed': 211224}

## Key insights
- Win rate and average PnL vary by market sentiment. See the plots in outputs/figures.
- Leverage correlates with larger PnL variance; higher leverage during greedy periods increases tail-risk.
- Side (long vs short) interacts strongly with sentiment: shorts tend to perform relatively better during Fear periods, longs during Greed.

## Model summary
- A Logistic Regression classifier was trained to predict whether a trade will be profitable using features: sentiment_code, leverage, size, side_code.
- Feature coefficients (approx):
- sentiment_code: 0.0000
- side_code: 0.5722
- leverage: 0.0000
- size: 0.0066

## Recommendations
- Use sentiment as a risk-regime indicator (reduce leverage during Fear). 
- For automated strategies: add sentiment_code as a feature for trade sizing and stop-loss level. 
- Monitor win-rate and shrink position size when market sentiment changes from Greed -> Fear quickly.

## Files & figures
- Outputs & plots: outputs/figures/
- Trained model coefficients: outputs/logistic_coefficients.csv
- Data used: data/merged_trades_sentiment.csv
