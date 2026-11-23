---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour return in the first hour after the 00:00 UTC funding settlement relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would take one position a day, at the close of the first hour after the 00:00 UTC settlement, against that hour's move and larger as the move is larger, and hold it a day, where the captured move (about 0.5 % for moves over one usual hourly move) is about 2.6 times the cost of a trade.
Why:
- F1: The book did not trade the signal. Its position had the forecast's sign on only 49.6 % of bars, and its correlation with the forecast was 0.026. It changed sign 0.009 times a day and its trades lasted 1330 to 2068 hours on average, against the idea's 24-hour horizon. Its 1352 short trades lost 41.6 % on average and its 797 long trades gained 29.7 %. So the failing Calmar (-0.099, a yearly return of -9.6 %) and the gap to holding's Sharpe (-0.37) come from months-long directional positions, not from the hourly-shock reversal.
- F2: The idea traded as it is stated is too small for the cost. A graded position held 24 hours from the step-5 grid gains 0.087 % per case before costs (t 4.5, 16958 cases) and only 0.013 % after a full 0.19 % turn. Its measured size, 0.12 % per case, is 0.6 times the cost of a trade.
- F3: The whole effect sits in the bar that opens at 00:00 UTC, the first hour after the daily settlement.
- F4: The reversal is graded only in the first hour after a settlement (bars opening at 00, 08 and 16 UTC).
