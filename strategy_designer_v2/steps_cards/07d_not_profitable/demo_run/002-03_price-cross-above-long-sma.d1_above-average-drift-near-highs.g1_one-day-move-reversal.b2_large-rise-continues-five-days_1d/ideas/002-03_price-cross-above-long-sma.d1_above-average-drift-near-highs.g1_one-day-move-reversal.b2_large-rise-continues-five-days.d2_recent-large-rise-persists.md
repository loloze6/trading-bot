---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's largest one-day rise of the past 5 days relative to the standard deviation of its daily returns over the past 20 days, the larger its rise over the next 5 days.
Consequence: A trader would hold a long for several days after an unusually large rise rather than drop it at the first down day, which avoids paying to re-enter.
Why:
- F1: The book lost money because fees ate more than the whole gross gain: the position earned 0.000227 a bar before costs and paid 0.000361 a bar in fees, so the book's mean daily return was -0.000135 (Sharpe -0.20) against 0.00118 (Sharpe 0.55) for holding the coins.
- F2: Fees are high because the forecast lives for only one day: runs of positive forecast last a median of 1 day (mean 1.87, over 4,759 runs), turnover is 0.333 of the book per bar, and entries plus exits make 4,307 of the 5,841 units of turnover.
- F3: The day right after the signal goes against the bet and the continuation comes later: the excess return on day 1 after a positive forecast is -0.00154 (t -3.0, n 8,849), days 2 to 4 are positive (+0.00086, +0.00037, +0.00083), and the 5-day slope on forecast rises from t 2.37 to t 3.39 (n 1,660) when the 5 days start one day later.
