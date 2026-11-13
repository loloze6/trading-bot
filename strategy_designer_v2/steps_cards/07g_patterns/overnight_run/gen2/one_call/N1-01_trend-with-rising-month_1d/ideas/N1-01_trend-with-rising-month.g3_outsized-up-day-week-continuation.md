---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-01_trend-with-rising-month
line: 7.g patterns
backtest: N1-01_trend-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin closes up by more than about two and a half times its trailing 20-day volatility, it keeps rising over the following five days, even though the very next day shows no gain.
Consequence: A trader can buy into an outsized up day rather than fade it, expecting gains over the following week rather than the next session.
Why:
- F5: After a day that rises more than 2.5 times trailing volatility, the next day is flat (+0.03%, n=315, t=0.09), but the next 5 days drift up +3.86% (non-overlapping, n=65, t=2.16), against +0.57% after ordinary days.
