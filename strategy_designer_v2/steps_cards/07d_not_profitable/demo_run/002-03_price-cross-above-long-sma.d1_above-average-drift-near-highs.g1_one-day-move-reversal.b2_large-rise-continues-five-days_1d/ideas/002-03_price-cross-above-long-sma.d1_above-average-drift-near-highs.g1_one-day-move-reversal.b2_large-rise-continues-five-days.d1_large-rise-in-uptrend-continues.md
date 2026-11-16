---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day rise relative to the standard deviation of its daily returns over the past 20 days, the larger its further rise over the next 5 days, only while the coin's 60-day return is positive, and the more so the higher that 60-day return.
Consequence: A trader would keep or add to a long after an unusually large one-day rise in a coin that is up over the past 60 days, and would refuse that trade in a coin that is down over 60 days.
Why:
- F1: The book lost money because fees ate more than the whole gross gain: the position earned 0.000227 a bar before costs and paid 0.000361 a bar in fees, so the book's mean daily return was -0.000135 (Sharpe -0.20) against 0.00118 (Sharpe 0.55) for holding the coins.
- F4: Only the largest rises carry the effect: the top fifth of positive forecasts is followed by a +0.0100 5-day excess return, while the middle fifths are followed by -0.0031 and -0.0043, yet the book still holds 0.21 to 0.40 allocation on those losing middle fifths.
- F5: The effect lives in coins already in an uptrend: the 5-day slope on forecast has t 2.90 (n 447) when the 60-day return is positive and t 0.15 (n 367) when it is not; signals in the lowest quarter of 20-day return are followed by a -0.0058 5-day excess against +0.0094 in the highest quarter.
- F6: What the book earns before fees comes from the market's rise, not from timing: the market part is +0.000286 a bar and the timing part is -0.000061.
