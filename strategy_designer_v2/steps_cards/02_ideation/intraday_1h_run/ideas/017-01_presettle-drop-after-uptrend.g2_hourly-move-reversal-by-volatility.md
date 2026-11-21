---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's last 1-hour return relative to its 24-hour volatility, the more its return over the next 1 hour runs the opposite way.
Consequence: A trader would take a short-lived position against an unusually large hourly move, larger as the move is larger relative to recent volatility.
Why:
- F2: Hourly moves reverse. Sorting each past 1-hour return by the coin's 24-hour volatility, the bottom decile is followed by +4.6 bp excess next hour (t 7.1, n 41,310) and the top deciles by -1.6 to -3.2 bp (t -2.6 to -6.5). The slope is negative in every year from 2018 to 2025 (t -0.7 to -7.5) and in LTC, XMR, XRP and ZEC (t -5.0 to -7.8), but not in BTC (t -1.1) or ETH (t 0.1).
