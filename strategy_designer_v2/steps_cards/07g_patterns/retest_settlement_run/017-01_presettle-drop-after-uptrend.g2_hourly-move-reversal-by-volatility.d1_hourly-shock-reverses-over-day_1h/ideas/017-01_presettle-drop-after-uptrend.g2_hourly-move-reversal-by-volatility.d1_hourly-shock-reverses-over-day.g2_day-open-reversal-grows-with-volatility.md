---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 24-hour volatility relative to its 30-day volatility, the larger the share of its first-hour move of the UTC day that it gives back over the next 24 hours.
Consequence: A trader would size a bet against the first UTC hour's move up when short-term volatility is high against its monthly level, and down when it is low.
Why:
- F2: The first-hour reversal is graded and larger than a trade's cost. Over the next 24 hours, the move against that hour's return rises with |z1| quintile: +0.05 %, +0.23 %, +0.30 %, +0.43 %, +0.47 % (t 0.7 to 5.1, about 3,417 cases each). The total move is the same, since the drift is about 0, and the top quintile is 2.4 times the 0.19 % cost. The tested idea as a whole moved +0.12 % per case, 0.6 times that cost.
- F4: The hour-0 reversal grows with the volatility level and builds over the day:
