---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour return in the first hour after any funding settlement (00:00, 08:00 or 16:00 UTC) relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would fade the move of the first hour after each settlement for a day, larger as the move is larger, and leave the other hours of the day alone, since they carry no reversal.
Why:
- F2: The idea traded as it is stated is too small for the cost. A graded position held 24 hours from the step-5 grid gains 0.087 % per case before costs (t 4.5, 16958 cases) and only 0.013 % after a full 0.19 % turn. Its measured size, 0.12 % per case, is 0.6 times the cost of a trade.
- F4: The reversal is graded only in the first hour after a settlement (bars opening at 00, 08 and 16 UTC).
