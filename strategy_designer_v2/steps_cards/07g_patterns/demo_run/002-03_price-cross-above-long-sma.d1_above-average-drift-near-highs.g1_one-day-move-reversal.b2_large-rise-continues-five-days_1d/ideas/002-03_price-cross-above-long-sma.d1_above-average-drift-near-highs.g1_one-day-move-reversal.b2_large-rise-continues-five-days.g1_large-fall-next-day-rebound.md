---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to the standard deviation of its daily returns over the past 20 days, the larger its rise over the next 1 day.
Consequence: A trader would buy into an unusually large one-day drop for a one-day rebound rather than sell it or stand aside.
Why:
- F1: Large down days are followed by a next-day rebound. Among down days, the slope of next-day excess return on the 20-day-volatility-scaled one-day move is -0.00391 (t=-4.55, n=7529), so bigger falls see bigger rebounds. Days scaled below -2 earn +0.74% next day (t=2.32, n=425), and days between -2 and -1 earn +0.55% (t=4.06, n=1511). The slope is negative in all six coins (XMR t=-3.85, XRP t=-2.33, ZEC t=-2.00). By year it is strong in 2018, 2020 and 2021 (t=-2.04, -4.30, -4.03) but near zero in 2022 and 2024.
- F4: The book loses on timing. Its mean bar gain is 0.000116, of which 0.000282 is the market's own rise and -0.000168 is timing. Positions of 0.16 and 0.50 are held after small up days, whose next-day returns are -0.08% and -0.16%. After down days the position is about 0, although the next day returns +0.69% after days scaled below -1.
