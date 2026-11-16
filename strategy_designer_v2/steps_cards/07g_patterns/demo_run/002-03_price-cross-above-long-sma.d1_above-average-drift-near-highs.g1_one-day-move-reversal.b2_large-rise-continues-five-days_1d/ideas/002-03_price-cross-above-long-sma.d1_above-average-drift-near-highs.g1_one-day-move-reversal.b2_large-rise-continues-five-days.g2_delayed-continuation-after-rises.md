---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day rise relative to the standard deviation of its daily returns over the past 20 days, the larger its rise from one day after that rise to five days after it.
Consequence: A trader would let the day after a large rise pass and then hold the long over the following four days, rather than buying at the rise's close.
Why:
- F3: The continuation the idea found shows up on days 2 to 5, not on day 1. After up days, the next-day excess slope on the scaled move is flat (t=1.14, n=7675). Small rises scaled 0 to 0.5 and 0.5 to 1 are followed by negative next-day excess returns (-0.19%, t=-2.34; -0.26%, t=-2.73). Over days 2 to 5 the slope is positive (0.0076, t=2.04, n=1422). Rises scaled 1 to 2 return +1.39% over days 2 to 5, against +0.38% after rises scaled 0 to 0.5.
- F4: The book loses on timing. Its mean bar gain is 0.000116, of which 0.000282 is the market's own rise and -0.000168 is timing. Positions of 0.16 and 0.50 are held after small up days, whose next-day returns are -0.08% and -0.16%. After down days the position is about 0, although the next day returns +0.69% after days scaled below -1.
