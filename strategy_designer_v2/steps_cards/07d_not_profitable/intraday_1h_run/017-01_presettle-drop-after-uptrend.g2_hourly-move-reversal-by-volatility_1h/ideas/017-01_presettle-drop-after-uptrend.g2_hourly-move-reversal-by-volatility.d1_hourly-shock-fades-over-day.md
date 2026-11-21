---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
line: 7.d not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's last 1-hour return relative to its 24-hour volatility, the more its return runs the opposite way, with the reversal building beyond the next 1 hour to its largest size over the next 24 hours.
Consequence: A trader would fade unusually large hourly moves but hold the position for about a day rather than re-trading every hour, so the gain per trade exceeds its fees.
Why:
- F1: The book loses because fees swamp a real but tiny edge: per bar the position earns 0.79 bps before costs but pays 6.54 bps in fees, because it turns over 0.61 of the book every hour at 10.7 bps per unit of turnover (20.77 trades per day). That gives a mean daily return of -0.0136 and a Sharpe of -16.35, against holding's 0.55 over 2,898 days.
- F2: The one-hour reversal is real but far too small to trade hourly: the sign-adjusted next-hour return is 1.79 bps on average and 3.12 bps in the top quintile of |vol-scaled move| (slope t 11.48, 413,189 cases). Even the strongest hours earn under a third of the 10.7 bps it costs to turn the position over fully.
- F4: The forecast's information outlasts the hour it is traded on. For the top quintile of |forecast|, the sign-adjusted return is 5.78 bps over the next 4 hours (t 3.95, 21,204 non-overlapping cases) and 28.3 bps over the next 24 hours (t 3.62, 4,015 cases), against 2.63 bps over the next 1 hour.
