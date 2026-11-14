---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-01_weekday-of-coming-bar
line: 7.d not profitable
backtest: N2-01_weekday-of-coming-bar_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose close is above its close twenty days earlier tends to keep rising from Thursday's close through Monday's close, so the late-week and weekend days in an uptrend carry a positive drift.
Consequence: In an uptrend, hold the long across Thursday to the weekend as one position instead of a single one-day Saturday trade, which raises time invested and cuts fees per unit of gain.
Why:
- F4: The book is too small to pay: it is invested only on Friday bars (54.7% of Fridays, 0% on other weekdays), its mean absolute allocation is 0.075, and its mean daily return is 0.00026 against the coin's holding mean of 0.00119, so its Sharpe falls 0.09 short of holding.
- F6: Trades are one-day longs (1361 trades, all entered Friday, held 0.99 days, 51.7% winners) that gross 0.35% and net 0.25% each, so fees take about 29% of each trade's gain.
- F7: In an uptrend the drift spans several days around the weekend, not only Saturday: next-day returns when up20 are 0.0055 (t 3.74) on Thursday bars, 0.0075 (t 5.52) on Friday bars and 0.0032 (t 2.79) on Saturday bars; in down20 every weekday lies within |t| < 1.7, and Friday-to-Monday 3-day returns are 0.0115 (t 4.51, n 969 Fridays) up20 against 0.0025 (t 1.14, n 1045) down20.
